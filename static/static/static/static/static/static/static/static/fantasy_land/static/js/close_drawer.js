function printSection() {
  const content = document.getElementById('printable-area').innerHTML;
  const printWindow = window.open('', '', 'height=600,width=800');

  printWindow.document.write('<html><head><title>Print</title>');
  printWindow.document.write('<style>body { font-family: sans-serif; padding: 20px; }</style>');
  printWindow.document.write('</head><body>');
  printWindow.document.write(content);
  printWindow.document.write('</body></html>');

  printWindow.document.close();
  printWindow.print();
}
