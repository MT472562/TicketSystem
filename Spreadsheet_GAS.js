function TicketSystemInsert(NameColumn, PplColumn, OutputColumn,OutputURLColumn, RequestUrl, SheetName) {
  var EndPoint = "/api_new_data/api";
  var TicketList = [];
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SheetName); // シート名を指定する
  var data = sheet.getRange(NameColumn + ":" + PplColumn).getValues();
  var lastRow = sheet.getLastRow();
  for (var i = 0; i < lastRow; i++) {
    var ppl = Math.round(data[i][1]);
    var name = data[i][0]
    const incell = OutputColumn+(i+1)
    const incell_url = OutputURLColumn+(i+1)
    if ((name === "" || name===NaN) && (ppl === 0.0 ||ppl ===NaN)) {
      TicketList.push("数値が入力されていません");
      sheet.getRange(incell).setValue("数値が入力されていません");
      sheet.getRange(incell_url).setValue("数値が入力されていません");
    } else {
      var payload = {
        name: name,
        ppl: ppl
      };
      var options = {
        'method': 'post',
        'contentType': 'application/json',
        'payload': JSON.stringify(payload)
      };
      var response = UrlFetchApp.fetch(RequestUrl + EndPoint, options);
      var responseData = response.getContentText();
      TicketList.push(responseData);
      sheet.getRange(incell).setValue(responseData);
      sheet.getRange(incell_url).setValue(RequestUrl+"/preview/"+responseData.replaceAll('"', ''));
    }
  }
  Logger.log(TicketList);
  return;
}

TicketSystemInsert("A", "B", "C","D", "https://ed3f-2400-2652-305-9e00-141f-37e0-5f23-98f1.ngrok-free.app", "Sheet")