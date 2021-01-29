import React, { Component } from "react";
import { useForm } from "react-hook-form";
import { login, API_TOKEN } from "./../Api";
import { useHistory } from "react-router-dom";

export const LoginView = () => {
  const { register, handleSubmit } = useForm();
  const history = useHistory();

  const onSubmit = (data) => {
    login(data.username, data.password).then((response) => {
      if (response.status === 200) {
        console.log(`JWT TOKEN: ${response.data}`);
        window.localStorage.setItem(API_TOKEN, response.data.token);
        history.push("/");
      }
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input name="username" type="string" ref={register} />
      <input name="password" type="password" ref={register} />
      <input type="submit" className="primary" value="Anmelden" />
    </form>
  );
};
