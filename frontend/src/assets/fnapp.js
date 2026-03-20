// 等待 flutter_inappwebview 准备就绪
const waitForFlutterInAppWebView = () => {
    return new Promise((resolve) => {
        if (window.flutter_inappwebview?. _platformReady) {
            // 如果已经准备好了，直接返回
            resolve(window.flutter_inappwebview);
        } else {
            resolve({});
            // 否则，等待框架发出准备就绪的事件
            // window.addEventListener('flutterInAppWebViewPlatformReady', () => {
            //     console.debug('等待 flutter_inappwebview 准备就绪');
            //     resolve(window.flutter_inappwebview);
            // });
        }
    });
};

// 封装的调用原生 handler 的通用函数
async function callNativeHandler(handlerName, parameter = '') {
    // 1. 等待 WebView 连接准备就绪
    const flutterInAppWebView = await waitForFlutterInAppWebView();

    // 2. 检查 callHandler 方法是否存在
    if (!flutterInAppWebView?. callHandler) {
        console.error(`Native handler '${handlerName}' is not available.`);
        return null;
    }

    try {
        // 3. 调用原生 handler。如果参数是对象，需要 JSON.stringify
        const parameterToSend = typeof parameter === 'object' ? JSON.stringify(parameter) : parameter;
        const result = await flutterInAppWebView.callHandler(handlerName, parameterToSend);

        // 4. 处理返回值。从你的代码看，返回的是字符串，需要解析。
        if (result) {
            try {
                const parsedResult = JSON.parse(result);
                // 返回值通常包装在 'result' 字段中
                return parsedResult.result ? JSON.parse(parsedResult.result) : parsedResult;
            } catch (e) {
                // 如果不是 JSON，直接返回原始结果
                return result;
            }
        }
        return null;
    } catch (error) {
        console.error(`Error calling native handler '${handlerName}':`, error);
        return null;
    }
}

// --- 具体的 API 函数 ---

/**
 * 从 App 获取全局信息（如主题、语言等）
 * 对应代码中的 jM() 函数
 */
async function getAppMessage() {
    // handler 名称是 'getAppMessage'
    const result = await callNativeHandler('getAppMessage');
    // 处理结果，例如，如果返回了 nightMode，可以在这里应用
    // if (result?. nightMode) {
    //     document.body.setAttribute('theme-mode', result.nightMode);
    // }
    return result;
}

/**
 * 更新 App 窗口的标题
 * @param {string} title - 要设置的标题
 * 对应代码中的 FM() 函数
 */
async function updateTitle(title) {
    // handler 名称是 'updateTitle'，参数需要包装成 {title: ...} 的格式
    return callNativeHandler('updateTitle', { title: title });
}

/**
 * 获取用户信息
 * 对应代码中的 RM() 函数
 */
async function getUserMessage() {
    // handler 名称是 'getUserMessage'
    return callNativeHandler('getUserMessage');
}
/**
 * 设置退出页面时的提示信息
 * @param {Object|string} tips - 提示信息对象或字符串
 * 如果传空字符串或 null，则清除退出提示
 * 对应代码中的 MM() 函数
 */
async function setExitPageTips(tips) {
    // handler 名称是 'setExitPageTips'
    // 参数需要是 JSON 字符串
    return callNativeHandler('setExitPageTips', tips);
}

// --- 导出 API 函数 ---
export { getAppMessage, updateTitle, getUserMessage, setExitPageTips };

window.getAppMessage = getAppMessage;
// --- 使用示例 ---
async function initMyApp() {
    // 1. 获取应用信息，并设置主题
    const appInfo = await getAppMessage();
    console.log('App Info:', appInfo);

    // 2. 更新窗口标题
    await updateTitle('我的独立应用');

    // 3. 获取用户信息
    const userInfo = await getUserMessage();
    console.log('User Info:', userInfo);
}


// 在页面加载完成后执行
// document.addEventListener('DOMContentLoaded', initMyApp);