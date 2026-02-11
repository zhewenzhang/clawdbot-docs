const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///Users/dave/clawd/reports/群策科技_横排大字体_v6.html');
  await page.waitForLoadState('networkidle');
  await page.pdf({
    path: '/Users/dave/clawd/reports/群策科技_横排大字体_v6.pdf',
    format: 'A4', landscape: true,
    printBackground: true,
    margin: { top: '0mm', right: '0mm', bottom: '0mm', left: '0mm' }
  });
  console.log('Done!');
  await browser.close();
})();
