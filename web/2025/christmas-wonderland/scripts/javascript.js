// 1. Define the data arrays
window._Y = [
  [117],        
  [86],         
  [71],         
  [98, 115],    
  [70, 71],     
  [97]          
];

window._X = [
  106, 57, 108, 90, 48, 78, 50, 88
];

// 2. Execute the fixed decoding logic
(function(){

  var hiddenZ = [57,86,50,90];

  // Decode Part 4 (_X reversed)
  var p4 = window._X.slice().reverse().map(c => String.fromCharCode(c)).join('');

  // Decode Part 5 (FIXED: Removed arr.reverse() on inner arrays)
  var merged = [];
  window._Y.forEach(arr => merged = merged.concat(arr)); // Changed here
  merged.reverse(); // Only reverse the final merged array
  var p5 = merged.map(c => String.fromCharCode(c)).join('');

  // Decode Part 6 (hiddenZ reversed)
  var p6 = hiddenZ.reverse().map(c => String.fromCharCode(c)).join('');

  // 3. Output the results
  console.log("%c[Cozy] Fixed Script Results:", "color:#4caf50; font-weight:bold; font-size:14px");
  
  // Log the raw Base64 parts
  console.log("Base64 Parts:", p4, p5, p6);
  
  // Log the decoded strings
  try {
      console.log("Decoded P4:", atob(p4));
      console.log("Decoded P5:", atob(p5)); // Should now be 'hallen'
      console.log("Decoded P6:", atob(p6));
      
      console.log("%cFull Suffix: " + atob(p4) + atob(p5) + atob(p6), "background: #222; color: #bada55; padding: 4px;");
  } catch (e) {
      console.error("Decoding failed:", e);
  }

})();