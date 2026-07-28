/**
 * pwa-icons.js — PWA Icon Generator for Notes Hub
 * =================================================
 * Run this script in a browser console (or paste it into DevTools)
 * to generate the two required PWA icons:
 *   - icon-192x192.png
 *   - icon-512x512.png
 *
 * The script creates inline canvases with the Notes Hub branding:
 * a green (#1a5e4a) circle background with a white book containing "NH" text.
 *
 * Save the downloaded files to Webpage/assets/
 */
(function () {
  'use strict';

  function createIcon(size) {
    var canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    var ctx = canvas.getContext('2d');

    // --- Background circle ---
    ctx.fillStyle = '#1a5e4a';
    ctx.beginPath();
    ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2);
    ctx.fill();

    // --- White book shape ---
    ctx.fillStyle = '#ffffff';
    var bookW = size * 0.5;
    var bookH = size * 0.6;
    var bookX = (size - bookW) / 2;
    var bookY = size * 0.2;
    var r = size * 0.08;

    // Rounded rectangle for the book
    ctx.beginPath();
    ctx.moveTo(bookX + r, bookY);
    ctx.lineTo(bookX + bookW - r, bookY);
    ctx.quadraticCurveTo(bookX + bookW, bookY, bookX + bookW, bookY + r);
    ctx.lineTo(bookX + bookW, bookY + bookH - r);
    ctx.quadraticCurveTo(bookX + bookW, bookY + bookH, bookX + bookW - r, bookY + bookH);
    ctx.lineTo(bookX + r, bookY + bookH);
    ctx.quadraticCurveTo(bookX, bookY + bookH, bookX, bookY + bookH - r);
    ctx.lineTo(bookX, bookY + r);
    ctx.quadraticCurveTo(bookX, bookY, bookX + r, bookY);
    ctx.fill();

    // --- Book spine line ---
    ctx.strokeStyle = '#1a5e4a';
    ctx.lineWidth = size * 0.02;
    ctx.beginPath();
    ctx.moveTo(bookX + bookW * 0.45, bookY + size * 0.04);
    ctx.lineTo(bookX + bookW * 0.45, bookY + bookH - size * 0.04);
    ctx.stroke();

    // --- "NH" text ---
    ctx.fillStyle = '#1a5e4a';
    ctx.font = 'bold ' + Math.round(size * 0.22) + 'px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('NH', size / 2, size * 0.68);

    // --- Trigger download ---
    var link = document.createElement('a');
    link.download = 'icon-' + size + 'x' + size + '.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
  }

  createIcon(192);
  createIcon(512);
  console.log('PWA icons generated! Save the downloaded files to Webpage/assets/');
})();
