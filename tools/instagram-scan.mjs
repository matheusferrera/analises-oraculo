import { chromium } from 'playwright';
import fs from 'node:fs/promises';

const handle = process.argv[2] || 'drajoanatavares';
const outDir = process.argv[3] || 'JoanaTavares';
const maxPostDetails = Number(process.argv[4] || 36);
const url = `https://www.instagram.com/${handle}/`;

await fs.mkdir(`${outDir}/data`, { recursive: true });
await fs.mkdir(`${outDir}/screenshots`, { recursive: true });

const browser = await chromium.launch({
  channel: 'chrome',
  headless: true,
  args: ['--disable-blink-features=AutomationControlled', '--no-sandbox'],
});

const page = await browser.newPage({
  viewport: { width: 1440, height: 1600 },
  locale: 'pt-BR',
  userAgent:
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
});

const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
await page.waitForTimeout(6000);

const closeButtons = [
  'svg[aria-label="Fechar"]',
  'svg[aria-label="Close"]',
  'div[role="button"] svg[aria-label="Fechar"]',
  'div[role="button"] svg[aria-label="Close"]',
];
for (const selector of closeButtons) {
  const btn = page.locator(selector).first();
  const count = await btn.count().catch(() => 0);
  if (count > 0) {
    await btn.click({ timeout: 3000, force: true }).catch(() => {});
    await page.waitForTimeout(1200);
    break;
  }
}

for (let i = 0; i < 5; i += 1) {
  await page.mouse.wheel(0, 1200);
  await page.waitForTimeout(1200);
}

const title = await page.title().catch(() => '');
const currentUrl = page.url();
const status = response?.status() || null;

await page.screenshot({ path: `${outDir}/screenshots/${handle}-profile.png`, fullPage: true });

const extracted = await page.evaluate(() => {
  const meta = {};
  for (const el of document.querySelectorAll('meta')) {
    const key = el.getAttribute('property') || el.getAttribute('name');
    if (key) meta[key] = el.getAttribute('content') || '';
  }

  const links = [...document.querySelectorAll('a[href]')]
    .map((a) => ({
      href: a.href,
      text: (a.innerText || a.getAttribute('aria-label') || '').trim(),
      imgAlt: [...a.querySelectorAll('img[alt]')].map((img) => img.getAttribute('alt')).filter(Boolean),
    }))
    .filter((item) => item.href.includes('/p/') || item.href.includes('/reel/'))
    .slice(0, 80);

  const images = [...document.querySelectorAll('img[alt]')]
    .map((img) => ({
      alt: img.getAttribute('alt') || '',
      src: img.currentSrc || img.src || '',
    }))
    .filter((item) => item.alt)
    .slice(0, 140);

  const scripts = [...document.querySelectorAll('script')]
    .map((script) => script.textContent || '')
    .filter((text) => text.includes('edge_followed_by') || text.includes('biography') || text.includes('followers'));

  return {
    meta,
    bodyText: document.body.innerText,
    links,
    images,
    scripts: scripts.slice(0, 5),
  };
});

const postDetails = [];
for (const item of extracted.links.slice(0, maxPostDetails)) {
  const postPage = await browser.newPage({
    viewport: { width: 1280, height: 1200 },
    locale: 'pt-BR',
    userAgent:
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  });
  try {
    const postResponse = await postPage.goto(item.href, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await postPage.waitForTimeout(3500);
    const detail = await postPage.evaluate(() => {
      const meta = {};
      for (const el of document.querySelectorAll('meta')) {
        const key = el.getAttribute('property') || el.getAttribute('name');
        if (key) meta[key] = el.getAttribute('content') || '';
      }
      return {
        title: document.title,
        bodyText: document.body.innerText,
        meta,
        time: document.querySelector('time')?.getAttribute('datetime') || '',
      };
    });
    postDetails.push({
      href: item.href,
      gridAlt: item.imgAlt?.[0] || '',
      status: postResponse?.status() || null,
      ...detail,
    });
  } catch (error) {
    postDetails.push({ href: item.href, gridAlt: item.imgAlt?.[0] || '', error: error.message });
  } finally {
    await postPage.close().catch(() => {});
  }
}

await fs.writeFile(`${outDir}/data/${handle}-scan.json`, JSON.stringify({
  scannedAt: new Date().toISOString(),
  url,
  currentUrl,
  status,
  title,
  ...extracted,
  postDetails,
}, null, 2));

await fs.writeFile(`${outDir}/data/${handle}-body.txt`, extracted.bodyText || '');

console.log(JSON.stringify({
  scannedAt: new Date().toISOString(),
  url,
  currentUrl,
  status,
  title,
  bodyLength: extracted.bodyText?.length || 0,
  links: extracted.links.length,
  images: extracted.images.length,
  postDetails: postDetails.length,
  screenshot: `${outDir}/screenshots/${handle}-profile.png`,
  json: `${outDir}/data/${handle}-scan.json`,
}, null, 2));

await browser.close();
