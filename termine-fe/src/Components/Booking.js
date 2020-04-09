import React from "react";
import { useForm } from "react-hook-form";
import { INFOBOX_STATES } from "../utils";

const renderInputRequired = () => (
  <span className="hintLabel">Dies ist ein Pflichtfeld</span>
);

export default function Booking({
  onBook,
  onCancel,
  startDateTime,
  claimToken,
  disable,
  state,
  setState,
  inputRef,
}) {
  const { register, handleSubmit, reset, errors } = useForm();

  const updateField = (e) => {
    setState({
      ...state,
      [e.target.id]: e.target.value,
    });
  };

  const onFocusHandler = () => {
    setState({
      ...state,
      infoboxState: INFOBOX_STATES.FORM_INPUT,
    });
  };

  const localOnBook = (data) => {
    onBook({ ...data, claimToken, startDateTime });
  };

  const { office, firstName, name, phone } = state;
  return (
    <form
      className={disable ? "disabled" : ""}
      onSubmit={handleSubmit(localOnBook)}
      ref={inputRef}
      onFocus={() => onFocusHandler()}
    >
      <fieldset className="input-group vertical">
        <legend>Terminbuchung</legend>
        <label htmlFor="firstName" className="displayFlex">
          Vorname {errors.firstName && renderInputRequired()}
        </label>
        <input
          id="firstName"
          name="firstName"
          readOnly={disable}
          disabled={disable}
          onChange={updateField}
          value={firstName}
          ref={register({ required: true })}
        />
        <label htmlFor="name" className="displayFlex">
          Name {errors.name && renderInputRequired()}
        </label>
        <input
          id="name"
          name="name"
          readOnly={disable}
          disabled={disable}
          onChange={updateField}
          value={name}
          ref={register({ required: true })}
        />
        <label htmlFor="phone" className="displayFlex">
          Handy-Nummer {errors.phone && renderInputRequired()}
        </label>
        <input
          id="phone"
          name="phone"
          readOnly={disable}
          disabled={disable}
          onChange={updateField}
          value={phone}
          ref={register({ required: true })}
        />
        <label htmlFor="office" className="displayFlex">
          Behörde {errors.office && renderInputRequired()}
        </label>
        <input
          id="office"
          name="office"
          readOnly={disable}
          disabled={disable}
          onChange={updateField}
          value={office}
          ref={register({ required: true })}
        />
        <input
          type="submit"
          className="primary"
          id="submit"
          value="Termin buchen"
          disabled={disable}
          style={{ fontSize: "1.2em" }}
        />
        <input
          type="button"
          className="secondary"
          id="cancel"
          value="Abbrechen"
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
