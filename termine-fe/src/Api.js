import axios from "axios";
import config from "./config";

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
    phone: data.phone,
  });
};

export const logout = () => {
  // credits go to https://stackoverflow.com/a/12866277
  const redirect = "/";
  const logout_success = "/logout_success";
  const username = "logout";
  const password = "logoutPasswordThatWillNeverExistsForReal";
  let xmlhttp = null;

  if (window["XMLHttpRequest"]) {
    xmlhttp = new window["XMLHttpRequest"]();
  }
  // code for IE
  else if (window["ActiveXObject"]) {
    xmlhttp = new window["ActiveXObject"]("Microsoft.XMLHTTP");
  }

  if (
    document.queryCommandSupported("ClearAuthenticationCache") &&
    document.queryCommandEnabled("ClearAuthenticationCache")
  ) {
    // IE clear HTTP Authentication
    document.execCommand("ClearAuthenticationCache");
    window.location.href = redirect;
  } else {
    xmlhttp.open("GET", logout_success, true, username, password);
    xmlhttp.send("");
    xmlhttp.onreadystatechange = function () {
      if (xmlhttp.readyState === 4) {
        window.location.href = redirect;
      }
    };
  }

  return false;
};

export const fetchBooked = (startDate, endDate) => {
  return axios.get(config.API_BASE_URL + "/booked", {
    params: {
      start_date: startDate,
      end_date: endDate,
    },
  });
};
