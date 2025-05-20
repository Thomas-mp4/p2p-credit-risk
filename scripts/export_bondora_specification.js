/**
 * This script extracts data from the Bondora specification page,
 * and saves it as both JSON and CSV files.
 * (https://api.bondora.com/doc/ResourceModel?modelName=PublicDatasetItem&v=1)
 */

(function() {
  // 1. Extract the data
  const rows = document.querySelectorAll('table.help-page-table tbody tr');
  const data = Array.from(rows).map(row => {
    const [nameTd, descTd, typeTd, infoTd] = row.querySelectorAll('td');
    return {
      name: nameTd.textContent.trim(),
      description: descTd.textContent.trim().replace(/\s+/g, ' '),
      type: typeTd.textContent.trim(),
      additionalInfo: infoTd.textContent.trim().replace(/\s+/g, ' ')
    };
  });

  // 2. Save JSON
  const jsonBlob = new Blob(
    [JSON.stringify(data, null, 2)],
    { type: 'application/json' }
  );
  const jsonUrl = URL.createObjectURL(jsonBlob);
  const jsonLink = document.createElement('a');
  jsonLink.href = jsonUrl;
  jsonLink.download = 'public_dataset_item.json';
  document.body.appendChild(jsonLink);
  jsonLink.click();
  URL.revokeObjectURL(jsonUrl);
  document.body.removeChild(jsonLink);

  // 3. Convert to CSV
  const csvHeaders = ['name', 'description', 'type', 'additionalInfo'];
  const csvRows = [
    csvHeaders.join(','), // header row
    ...data.map(item =>
      csvHeaders.map(key =>
        `"${(item[key] || '').replace(/"/g, '""')}"`
      ).join(',')
    )
  ];
  const csvBlob = new Blob([csvRows.join('\n')], { type: 'text/csv' });
  const csvUrl = URL.createObjectURL(csvBlob);
  const csvLink = document.createElement('a');
  csvLink.href = csvUrl;
  csvLink.download = 'public_dataset_item.csv';
  document.body.appendChild(csvLink);
  csvLink.click();
  URL.revokeObjectURL(csvUrl);
  document.body.removeChild(csvLink);
})();