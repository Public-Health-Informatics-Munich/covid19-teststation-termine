import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { addUser } from "../Api";

export default function AddUser({ onSuccess }) {
  const { register, handleSubmit, reset, errors, setError } = useForm();

  const onSave = (data) => {
    if (/\s/.test(data.newUserName)) {
      setError(
        "newUserName",
        "sanitize",
        "Keine Leerzeichen im Nutzernamen erlaubt."
      );
    } else if (data.newUserPassword !== data.newUserPasswordConfirm) {
      reset({ ...data, newUserPasswordConfirm: "" });
      setError(
        "newUserPasswordConfirm",
        "match",
        "Die Passwörter sind nicht identisch!"
      );
    } else {
      setLoading(true);
      addUser(data)
        .then(() => {
          reset();
          onSuccess();
          setSuccessUserName(data.newUserName);
          setTimeout((_) => setSuccessUserName(""), 6000);
        })
        .catch((error) => {
          if (error?.response?.status === 409) {
            reset({ ...data, newUserName: "" });
            setError(
              "users",
              "duplicate",
              "Ein Benutzer mit diesem Nutzernamen existiert bereits."
            );
          } else {
            setError(
              "network",
              "unknown",
              "Ein unbekannter Fehler ist aufgetreten, bitte Seite neu laden."
            );
          }
        })
        .then(() => {
          setLoading(false);
        });
    }
  };

  const [successUserName, setSuccessUserName] = useState("");
  const [loading, setLoading] = useState(false);

  return (
    <div className="row">
      <form onSubmit={handleSubmit(onSave)}>
        <h3>Neuen Benutzer anlegen:</h3>
        <div
          className="hintLabel"
          style={{ marginLeft: "var(--universal-margin)" }}
        >
          {errors.users && errors.users.message}
          {errors.network && errors.network.message}
          {errors.newUserName && errors.newUserName.message}
          {errors.newUserPasswordConfirm &&
            errors.newUserPasswordConfirm.message}
        </div>
        <div style={{ marginLeft: "var(--universal-margin)" }}>
          {successUserName &&
            `Der Benutzer "${successUserName}" wurde angelegt.`}
        </div>
        <input
          type="text"
          name="newUserName"
          placeholder="Benutzername"
          ref={register({ required: true })}
        />
        <input
          type="password"
          name="newUserPassword"
          placeholder="Passwort"
          ref={register({ required: true })}
        />
        <input
          type="password"
          name="newUserPasswordConfirm"
          placeholder="Passwort wiederholen"
          ref={register({ required: true })}
        />
        <input
          type="submit"
          name="submit"
          value={loading ? "Wird gespeichert..." : "Speichern"}
        />
      </form>
    </div>
  );
}
