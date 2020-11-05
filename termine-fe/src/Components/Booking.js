import React from "react";
import { Controller } from "react-hook-form";
import { Trans, t } from "@lingui/macro";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { InputRequired } from "./InputRequired";
import { AddressForm } from "./AddressForm";

import { registerLocale, setDefaultLocale } from "react-datepicker";
import de from "date-fns/locale/de";
registerLocale("de", de);
setDefaultLocale("de");

let reasons = require("../config/reasons.json");

export default function Booking({
  i18n,
  onBook,
  onCancel,
  startDateTime,
  claimToken,
  disable,
  form,
  inputRef,
}) {
  const startDate = new Date("1990-01-01");
  const { register, handleSubmit, reset, errors, control } = form;

  const localOnBook = (data) => {
    onBook({ ...data, claimToken, startDateTime });
  };

  const reasonItems = reasons.map((key) => (
    <option key={key} value={key}>
      {i18n._(key)}
    </option>
  ));

  return (
    <form
      className={disable ? "disabled" : ""}
      onSubmit={handleSubmit(localOnBook)}
      ref={inputRef}
    >
      <fieldset className="input-group vertical">
        <legend>
          <Trans>Booking</Trans>
        </legend>
        <label htmlFor="firstName" className="displayFlex">
          <Trans>Given Name</Trans> {errors.firstName && <InputRequired />}
        </label>
        <input
          name="firstName"
          readOnly={disable}
          disabled={disable}
          ref={register({ required: true })}
        />
        <label htmlFor="name" className="displayFlex">
          <Trans>Surname</Trans> {errors.name && <InputRequired />}
        </label>
        <input
          name="name"
          readOnly={disable}
          disabled={disable}
          ref={register({ required: true })}
        />
        <AddressForm form={form} disable={disable} />
        <label htmlFor="phone" className="displayFlex">
          <Trans>Mobile No.</Trans> {errors.phone && <InputRequired />}
        </label>
        <input
          name="phone"
          readOnly={disable}
          disabled={disable}
          ref={register({ required: true })}
        />
        {window.config.formFields.includes("dayOfBirth") && (
          <React.Fragment>
            <label htmlFor="dayOfBirth" className="displayFlex">
              <Trans>DayOfBirth</Trans> {errors.dayOfBirth && <InputRequired />}
            </label>
            <Controller
              name="dayOfBirth"
              control={control}
              defaultValue={startDate}
              render={(props) => (
                <DatePicker
                  showYearDropdown
                  showMonthDropdown
                  selected={props.value}
                  onChange={(selectedDate) => props.onChange(selectedDate)}
                  dropdownMode="select"
                  dateFormat="dd.MM.yyyy"
                  maxDate={new Date()}
                />
              )}
              rules={{ required: true }}
            />
          </React.Fragment>
        )}
        <label htmlFor="office" className="displayFlex">
          <Trans>Office</Trans> {errors.office && <InputRequired />}
        </label>
        <input
          name="office"
          readOnly={disable}
          disabled={disable}
          ref={register({ required: true })}
        />
        {window.config.formFields.includes("reason") && (
          <React.Fragment>
            <label htmlFor="reason" className="displayFlex">
              <Trans>Reason</Trans> {errors.reason && <InputRequired />}
            </label>
            <select
              id="reason"
              name="reason"
              ref={register({ required: true })}
            >
              {reasonItems}
            </select>
          </React.Fragment>
        )}
        <input
          type="submit"
          className="primary"
          id="submit"
          value={i18n._(t`Book Appointment`)}
          disabled={disable}
          style={{ fontSize: "1.2em" }}
        />
        <input
          type="button"
          className="secondary"
          id="cancel"
          value={i18n._(t`Cancel`)}
          disabled={disable}
          style={{ fontSize: "1.2em" }}
          onClick={() => {
            reset();
            onCancel();
          }}
        />
      </fieldset>
    </form>
  );
}
