import { add, format, parseISO } from "date-fns";
import { de } from "date-fns/locale";

export const formatDate = (ISOString) =>
  ISOString ? format(parseISO(ISOString), "PP", { locale: de }) : "";
export const formatTime = (ISOString, slotLengthMin) => {
  const date = parseISO(ISOString);
  return ISOString
    ? `${format(date, "p", { locale: de })} - ${format(
        add(date, { minutes: slotLengthMin }),
        "p",
        { locale: de }
      )}`
    : "";
};
export const formatStartTime = (ISOString) => {
  const date = parseISO(ISOString);
  return ISOString ? `${format(date, "p", { locale: de })}` : "";
};

export const ISOStringWithoutTimeZone = (date) => {
  const day = `${date.getDate()}`.padStart(2, "0");
  const month = `${date.getMonth() + 1}`.padStart(2, "0");
  const year = date.getFullYear();
  return `${year}-${month}-${day}`;
};

export const INFOBOX_STATES = {
  INITIAL: "description",
  FORM_INPUT: "input",
  APPOINTMENT_SUCCESS: "success",
  ERROR: "error",
};

export const parseJwt = (token) => {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );

    return JSON.parse(jsonPayload);
  } catch (e) {
    return {};
  }
};
