# RestAPI

Our REST API is a web-based API using a Websocket connection and was developed with algorithmic trading in mind. 

Developers and investors can create custom trading applications, integrate into our platform, back test strategies and build robot trading. Calls can be made in any language that supports a standard HTTP. 

We utilize the new OAuth 2.0 specification for authentication via token. This allows for a more secure authorization to access your application and can easily be integrated with web applications, mobile devices, and desktop platforms

With the use of the socket.io library, the API has streaming capability and will push data notifications in a JSON format. Your application will have access to our real-time streaming market data, subscribe in real time access to trading tables and place live trades.

## How to start:
1.	A FXCM account. You can apply for a demo account <a href="https://www.fxcm.com/">here</a> 
2.	A persistent access token. You can generate one from the <a href="https://tradingstation.fxcm.com/">Trading Station web</a>. Click on User Account > Token Management on the upper right hand of the website.
3.	Download Rest API word documents at <a href="https://apiwiki.fxcorporate.com/api/RestAPI/Socket%20REST%20API%20Specs.pdf">here</a>
4. Documents in Swagger format at <a href="https://fxcm.github.io/rest-api-docs/#">here</a> 
5. Start coding.  You will need to reference the <a href="https://socket.io/docs/client-api/">socket.io library</a> in your code. 
   a.	Using Javascript, click <a href="https://www.npmjs.com/package/socket.io">here</a>
   b.	 Using Python, click <a href="https://pypi.python.org/pypi/socketIO-client">here</a>
6. Sample code for Python at <a href="https://github.com/fxcm/fxcm-api-rest-python3-example">here</a> 
7. Sample code for Java Script at <a href="https://github.com/fxcm/fxcm-api-rest-nodejs-example">here</a>

## Real Case Study:

1. Learn how to run BT backtest on FXCM historical data via RestAPI at <a href="https://apiwiki.fxcorporate.com/api/StrategyRealCaseStudy/RestAPI/BT strategy on FXCM data.zip">here</a>. 
What is <a href="http://pmorissette.github.io/bt/">bt?</a> 
2. Learn how to run QSTrader on FXCM data via RestAPI at <a href="https://apiwiki.fxcorporate.com/api/StrategyRealCaseStudy/RestAPI/QSTrader on FXCM data.zip">here</a>. 
what is <a href="https://www.quantstart.com/qstrader">QSTrader?</a>
3. Building/back testing RSI strategy via RestAPI at <a href="https://apiwiki.fxcorporate.com/api/StrategyRealCaseStudy/RestAPI/RsiStrategy.zip">here</a>.
4. One video demonstrate how to backtest strategies in Visual Studio via FXCM data On QuantConnect LEAN platform at <a href="https://www.youtube.com/watch?v=m6llfznP4d4">here</a>

## Note:
o	This is for personal use and abides by our [EULA](https://www.fxcm.com/uk/forms/eula/)

o	For more information, you may contact us: api@fxcm.com

