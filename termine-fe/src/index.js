import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import "mini.css";
import App from "./App";
import * as serviceWorker from "./serviceWorker";
import envConfig from "./config";
import { BrowserRouter as Router } from "react-router-dom";
import detectBrowserLanguage from "detect-browser-language";
import { I18nProvider } from "@lingui/react";
import { setupI18n } from "@lingui/core";
import catalogEn from "./locales/en/messages";
import catalogDe from "./locales/de/messages";

const i18n = setupI18n();
const supportedLanguages = { en: catalogEn, de: catalogDe };
i18n.load(supportedLanguages);
const browserLanguage = detectBrowserLanguage().substring(0, 2);
const language = browserLanguage in supportedLanguages ? browserLanguage : "en";
i18n.activate(language);

ReactDOM.render(
  <React.StrictMode>
    <I18nProvider i18n={i18n}>
      <Router>
        <App i18n={i18n} />
      </Router>
    </I18nProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

envConfig.setup();
