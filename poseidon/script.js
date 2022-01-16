import fs from 'fs';
import draftToHtml from "draftjs-to-html";

function callback(err, content) {
  let rows = content.split('\n');

  let output = [];

  rows.forEach((row) => {

    if (!row) {
      return;
    }

    let [id, raw] = row.split('|');
    let converted = draftToHtml(JSON.parse(raw));

    output.push(`${id}|${converted}`);
  });

  output = output.join("\n");
  fs.writeFile("events.csv", output, (data) => {});
};


fs.readFile('here.csv', 'utf8', callback);