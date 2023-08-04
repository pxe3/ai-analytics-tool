import asyncio
from pyppeteer import launch
import openai

# Set your OpenAI API key here
openai.api_key = open("cgpt4 key.txt", "r").read()

async def scrape_with_puppeteer(url):
    browser = await launch(headless=True)
    page = await browser.newPage()

    try:
        # Set a timeout of 30 seconds for the page to load
        await page.goto(url, {'waitUntil': 'domcontentloaded', 'timeout': 30000})
        content = await page.evaluate('document.body.innerText')
    except Exception as e:
        print("Error occurred during scraping:", str(e))
        content = ""
    finally:
        await browser.close()

    return content

def generate_summary(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200
    )
    return response['choices'][0]['text']

def search_website(topic, website_name=None):
    openai_search_query = f"{topic} website"
    if website_name:
        openai_search_query += f" on {website_name}"
    search_results = openai.Engine("ada").search(
        model="text-davinci-002",
        query=openai_search_query,
        documents=3,
        return_prompt=True
    )
    for result in search_results["data"]:
        if result["score"] > 5.0:
            return result["document"]["text"]

    return None

if __name__ == "__main__":
    user_topic = input("Enter the topic you want analytics/trends on: ")
    user_website = input("Enter the website URL or name you want to scrape (press Enter if none): ").strip()

    try:
        # Search for the website using OpenAI
        website_url = search_website(user_topic, user_website)

        if not website_url:
            print(f"No relevant website found for '{user_topic}'.")
            scraped_content = ""
        else:
            # Scrape the website using pyppeteer
            loop = asyncio.get_event_loop()
            scraped_content = loop.run_until_complete(scrape_with_puppeteer(website_url))

            # Rest of the code for filtering and summarizing results
            sentences = scraped_content.split(". ")
            # Filter relevant sentences based on the user's topic
            relevant_sentences = [sentence for sentence in sentences if user_topic.lower() in sentence.lower()]

            if not relevant_sentences:
                print("No relevant information found on the given topic.")
            else:
                print("Relevant information:")
                for sentence in relevant_sentences:
                    print(sentence)

                # Summarize each relevant result using OpenAI
                summarized_results = [generate_summary(sentence) for sentence in relevant_sentences]

                print("\nSummarized results:")
                for summary in summarized_results:
                    print(summary)
    except Exception as e:
        print("Error occurred:", str(e))
