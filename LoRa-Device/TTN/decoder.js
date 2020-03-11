function Decoder(bytes, port) {
    // Decode an uplink message from a buffer
    // (array) of bytes to an object of fields.
    var decoded = {};
    
  function uintToString(uintArray) {
      var encodedString = String.fromCharCode.apply(null, uintArray),
          decodedString = decodeURIComponent(escape(encodedString));
      return decodedString;
  }
  
    decoded.value = uintToString(bytes)
    decoded.device = "Lora-device-1"
    decoded.message = "State change detected."
    return decoded;
  }