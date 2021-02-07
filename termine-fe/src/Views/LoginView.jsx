import { Trans } from "@lingui/macro";
import React from "react";
import { useForm } from "react-hook-form";
import { useHistory } from "react-router-dom";

export const LoginView = ({ login, error }) => {
  const { register, handleSubmit } = useForm();
  const history = useHistory();

  const onSubmit = (data) => {
    login(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label for="username">
        <Trans>Username</Trans>
        <input id="username" name="username" type="string" ref={register} />
      </label>
      <label for="password">
        <Trans>Password</Trans>
        <input id="password" name="password" type="password" ref={register} />
      </label>
      <input type="submit" className="primary" value="Anmelden" />
      {error && (
        <h1 className="card error fluid">
          <Trans>Wrong username or password</Trans>
        </h1>
      )}
    </form>
  );
};
