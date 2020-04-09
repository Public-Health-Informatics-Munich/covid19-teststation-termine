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
