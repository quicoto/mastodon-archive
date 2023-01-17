'use strict';

import * as fs from 'fs';
import * as utils from './src/utils.js';

const config = {
  distFolder: './dist',
};

let rawdata = fs.readFileSync('./archive/outbox.json');
let output = JSON.parse(rawdata);
let contentHTML = '';

/**
 * @param  {object} object
 * @param  {string} object.id
 * @param  {string} object.published
 * @param  {string} object.url
 * @param  {string} object.content
 */
function _item(object) {
  return `
  <div class="item">
    <div class="item__date"><a href="${object.url}" target="_blank" rel="noopener noreferrer">${utils.formatDate(object.published)}</a></div>
    <div class="item__content">${object.content}</div>
  </div>
  `;
}

const items = output.orderedItems.reverse();

for (let index = 0, len = items.length; index < len; index++) {
  const url = items[index].object?.url

  if (url) {
    contentHTML += _item(items[index].object)
  }
}

if (!fs.existsSync(config.distFolder)) {
  fs.mkdirSync(config.distFolder);
}

let template = utils.readFile('./src/template.html');

template = template.replace(`%CONTENT%`, contentHTML);

utils.createFile('index.html', config.distFolder, template);