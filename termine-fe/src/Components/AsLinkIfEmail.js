import React from "react";
import isEmail from "validator/lib/isEmail";

export const AsLinkIfEmail = ({ value }) =>
  isEmail(value) ? <a href={"mailto:" + value}>{" " + value}</a> : " " + value;
