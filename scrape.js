const puppeteer = require('puppeteer');
const fs = require('fs');
const { Configuration, OpenAIApi} = require('@openai/api')
require('dotenv').config()
console.log(process.env.OPENAI_API_KEY);
const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
  });
  const openai = new OpenAIApi(configuration);
  const api = new OpenAIApi(apiKey);


(async ( ) => {

    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.goto('https://liquipedia.net/')
    await page.screenshot({path: 'screenshot.png'});
    browser.close()
})();