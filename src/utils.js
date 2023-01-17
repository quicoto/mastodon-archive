import * as fs from 'fs';

export function readFile(path) {
  return fs.readFileSync(path, { encoding: 'utf8', flag: 'r' });
}

export function createFile(fileName, path, data) {
  const processedData = data.replaceAll('%VERSION%', process.env.npm_package_version);

  fs.writeFileSync(`${path}/${fileName}`, processedData);
}

export function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function formatRSSDate(date) {
  let newDate = new Date();

  if (date) newDate = new Date(date);

  return new Date(newDate).toUTCString();
}

