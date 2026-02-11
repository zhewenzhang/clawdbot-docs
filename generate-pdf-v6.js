const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto('file:///Users/dave/clawd/reports/STMicroelectronics_公司分析报告.html');
  await page.waitForLoadState('networkidle');
  
  await page.pdf({
    path: '/Users/dave/clawd/reports/STMicroelectronics_公司分析报告.pdf',
    format: 'A4',
    landscape: true,
    printBackground: true,
    margin: { top: '0mm', right: '0mm', bottom: '0mm', left: '0mm' }
  });
  
  console.log('PDF v6 已重新生成！');
  await browser.close();
})();
