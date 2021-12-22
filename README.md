Website Title: The Stock Portal
Website Link: https://the-stock-portal.herokuapp.com/
Financial Modeling Prep API Link: https://site.financialmodelingprep.com/developer/docs

The Stock Portal Description:
For my first capstone project for Springboard's software engineering career track I have decided 
to create an application that focuses on a personal interest of mine. The title of my website is "The Stock Portal." The data used is sourced from an API named the "Financial Modeling Prep." The website allows users to look up stock data in real time, track market performance, track stock sector performance, view a list of over 6000 stocks, and create a list of personally selected stocks that they can monitor on a daily basis.

The Stock Portal Features:
The main feature of my website is the ability to search for a stock by a ticker symbol and immediatley view the data and analytics relating to that stock. The data is requested in real time so the information on the screen is 100% up to date. When the user is viewing a stock's information, there is a button to track that specific stock. When the user clicks that button that specific stock will be added to their homepage under the stock search area. This will allow the user to log in and immediatley have access to a button for each of their tracked stocks so they can easily view each of those stock's information without having to search for them every time. Again upon clicking of a tracked stock they will be presented with that specific stock's information that is up to date at the time of viewing. At the bottom of the stock information page, there is a link to view more information about the company. Clicking on this link will provide a variety of information about the company including but not limited to the CEO's name, headquarter's location and number of employees. They can untrack a stock by clicking on the "Untrack this Stock" button on the stock information page. This will remove that specific stock from their homepage. If the user wants to search for a stock but does not know the stock's ticker symbol, there is a link on the homepage to view a full list of over 6000 stocks. They can search using the search bar and find the stock they need. This list includes the companies names, ticker symbol, and the stock exchange that the stock belongs to. This serves as an easy way to find out what the ticker symbol is for a specific stock.

The Stock Portal user flow:
Upon visiting the stock port the user will be redirected to the login page. If the user has not used The Stock Portal before there is a link to be redirected to the signup page. When the user logs in or signs up, they will be redirected to the homepage and presented with the homepage. The homepage is where the user can access the stock search input, view their tracked stocks, or view a list of tracked stocks. The homepage has a navbar with links that can direct them to view current S&P 500 market performance data, view stock sector performance data, view and edit their profile information, and logout. 

The Stock Portal stack:
The languages used to create this application include Python-Flask for the backend route/view functions. The RDBMS used is PostgreSQL and the data is manipulated using Flask-SQLAlchemy. The templates are rendered using Jinja and CSS/Bootstrap is used for the styling.




