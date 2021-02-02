import axios from "axios";
import config from "./config";

export const API_TOKEN = "token";

axios.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    if (401 === error.response.status) {
      window.location = "/#/login";
    } else {
      return Promise.reject(error);
    }
  }
);

axios.interceptors.request.use(function (config) {
  const token = window.localStorage.getItem(API_TOKEN);
  if (token !== null) {
    config.headers["Authorization"] = token;
  }

  return config;
});

export const login = (username, password) => {
  return axios.post("/login", {
    username: username,
    password: password,
  });
};

export const loggedIn = () => {
  return window.localStorage[API_TOKEN] !== null;
};

export const fetchSlots = () => {
  return axios.get(config.API_BASE_URL + "/next_free_slots");
};

export const claimSlot = (startDateTime) => {
  return axios.get(config.API_BASE_URL + "/claim_appointment", {
    params: {
      start_date_time: startDateTime,
    },
  });
};

export const unClaimSlot = (claimToken) => {
  return axios.delete(config.API_BASE_URL + "/claim_token", {
    params: {
      claim_token: claimToken,
    },
  });
};

export const book = (data) => {
  return axios.post(config.API_BASE_URL + "/book_appointment", {
    start_date_time: data.startDateTime,
    claim_token: data.claimToken,
    office: data.office,
    first_name: data.firstName,
    name: data.name,
    street: data.street,
    street_number: data.streetNumber,
    post_code: data.postCode,
    city: data.city,
    phone: data.phone,
    birthday: data.dayOfBirth,
    reason: data.reason,
  });
};

export const deleteBooking = (id) => {
  return axios.delete(config.API_BASE_URL + "/booking", {
    params: {
      booking_id: id,
    },
  });
};

export const logout = () => {
  window.localStorage.removeItem(API_TOKEN);
};

export const fetchBooked = (startDate, endDate) => {
  return axios.get(config.API_BASE_URL + "/booked", {
    params: {
      start_date: startDate,
      end_date: endDate,
    },
  });
};

export const changePassword = (
  old_user_password,
  new_user_password,
  new_user_password_confirm
) => {
  return axios.patch(config.API_BASE_URL + "/user", {
    old_user_password,
    new_user_password,
    new_user_password_confirm,
  });
};
