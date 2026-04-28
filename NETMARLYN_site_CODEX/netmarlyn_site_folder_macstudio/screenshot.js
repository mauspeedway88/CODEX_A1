const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    await page.goto('http://localhost:8080/index.html');
    await page.screenshot({ path: '/Users/mauricio/.gemini/antigravity/brain/8109f6e6-5789-43bb-a835-8555e8b17217/index_screenshot.png' });
    
    await page.goto('http://localhost:8080/videos.html');
    await page.screenshot({ path: '/Users/mauricio/.gemini/antigravity/brain/8109f6e6-5789-43bb-a835-8555e8b17217/videos_screenshot.png' });

    await browser.close();
})();
