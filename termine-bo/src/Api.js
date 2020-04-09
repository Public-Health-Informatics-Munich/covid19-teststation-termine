import axios from "axios";
import config from "./config";

export const fetchUsers = () => {
    return axios.get(config.API_BASE_URL + '/user');
};

export const patchUser = (data) => {
    return axios.patch(config.API_BASE_URL + '/user', {...data});
};
