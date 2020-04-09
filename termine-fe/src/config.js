import Axios from "axios";

const dev = {
  API_BASE_URL: "/api",
  setup: () => {
    Axios.interceptors.request.use(
      function (config) {
        const user = window.localStorage.user;
        const pass = window.localStorage.pass;
        if (user && pass) {
          const token = Buffer.from(`${user}:${pass}`, "utf8").toString(
            "base64"
          );
          config.headers.Authorization = `Basic ${token}`;
        }
        return config;
      },
      function (error) {
        return Promise.reject(error);
      }
    );
  },
};

const prod = {
  API_BASE_URL: "/api",
  setup: () => {},
};

const config = process.env.REACT_APP_STAGE === "prod" ? prod : dev;

export default {
  // Add common config values here
  ...config,
};
