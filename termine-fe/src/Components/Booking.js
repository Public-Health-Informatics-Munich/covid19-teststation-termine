import React from "react";
import { Controller } from "react-hook-form";
import { Trans, t } from "@lingui/macro";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
let reasons = require("../config/reasons.json");

const renderInputRequired = () => (
  <span className="hintLabel">
    <Trans>This input is required.</Trans>
  </span>
);

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
          <Trans>Given Name</Trans> {errors.firstName && renderInputRequired()}
        </label>
        <input
          name="firstName"
          readOnly={disable}
          disabled={disable}
          ref={register({ required: true })}
        />
        <label htmlFor="name" className="displayFlex">
          <Trans>Surname</Trans> {errors.name && renderInputRequired()}
        </label>
        <input
          name="name"
          readOnly={disable}
          disabled={disable}
          ref={register({ required: true })}
        />
        <fieldset className="input-group vertical">
          <legend>
            <Trans>Home Address</Trans>
          </legend>
          <div className="displayFlex vertical">
            <div className="displayFlex justifyBetween">
              <label htmlFor="street">
                <Trans>Street</Trans> {errors.street && renderInputRequired()}
              </label>
              <label htmlFor="streetnumber">
                <Trans>StreetNumber</Trans>{" "}
                {errors.streetNumber && renderInputRequired()}
              </label>
            </div>
            <div className="displayFlex">
              <input
                name="street"
                className="width80Percent"
                readOnly={disable}
                disabled={disable}
                ref={register({ required: true })}
              />
              <input
                name="streetNumber"
                className="width20Percent"
                readOnly={disable}
                disabled={disable}
                ref={register({ required: true })}
              />
            </div>
          </div>
          <div className="displayFlex vertical">
            <div className="displayFlex justifyBetween">
              <label htmlFor="postCode">
                <Trans>PostCode</Trans>{" "}
                {errors.postCode && renderInputRequired()}
              </label>
              <label htmlFor="city">
                <Trans>City</Trans> {errors.city && renderInputRequired()}
              </label>
            </div>
            <div className="displayFlex">
              <input
                name="postCode"
                className="width20Percent"
                readOnly={disable}
                disabled={disable}
                ref={register({ required: true })}
              />
              <input
                name="city"
                className="width80Percent"
                readOnly={disable}
                disabled={disable}
                ref={register({ required: true })}
              />
            </div>
          </div>
        </fieldset>
        <label htmlFor="phone" className="displayFlex">
          <Trans>Mobile No.</Trans> {errors.phone && renderInputRequired()}
        </label>
        <input
          name="phone"
          readOnly={disable}
          disabled={disable}
          ref={register({ required: true })}
        />
        <label htmlFor="dayOfBirth" className="displayFlex">
          <Trans>DayOfBirth</Trans> {errors.dayOfBirth && renderInputRequired()}
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
              maxDate={new Date()}
            />
          )}
          rules={{ required: true }}
        />
        <label htmlFor="office" className="displayFlex">
          <Trans>Office</Trans> {errors.office && renderInputRequired()}
        </label>
        <input
          name="office"
          readOnly={disable}
          disabled={disable}
          ref={register({ required: true })}
        />
        <label htmlFor="reason" className="displayFlex">
          <Trans>Reason</Trans> {errors.reason && renderInputRequired()}
        </label>
        <select id="reason" name="reason" ref={register({ required: true })}>
          {reasonItems}
        </select>
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
