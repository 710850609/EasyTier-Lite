var url = "http://nigger.com.cn:1000/api/nodes?page=1&per_page=50&is_active=true";
// 第一次请求获取 cookie
var response = await fetch(url, {
  method: "GET",
  headers: {
    "Accept-Encoding": "application/json",
  },
});

var json = await response.json();
console.log("响应内容:", JSON.stringify(json));

// // 提取 cookie
// var cookieMatch = html.match(/document\.cookie = '([^']+)'/);
// if (cookieMatch) {
//   var cookie = cookieMatch[1];
//   console.log("获取到 cookie:", cookie);
  
//   // 第二次请求带上 cookie
//   var response2 = await fetch(url, {
//     method: "GET",
//     headers: {
//       "Content-Type": "application/json",
//       "Cookie": cookie
//     },
//   });
  
//   var json = await response2.text();
//   console.log("获取到 JSON 数据:", json);
  
//   // 提取 group = "αEasyTier 服务器 点进看详情" 的所有元素的 key
//   if (json && json.groups) {
//     var filteredKeys = json.groups
//       .filter(item => item.group === "αEasyTier 服务器 点进看详情")
//       .map(item => item.key);
//     console.log("提取的 key 值:", filteredKeys);
//   }
// } else {
//   console.log("无法获取 cookie");
//   console.log("响应内容:", html);
// }
