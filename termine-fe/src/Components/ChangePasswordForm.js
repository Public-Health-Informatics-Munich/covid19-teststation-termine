import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { changePassword } from "../Api";
import FocusLock from "react-focus-lock";
import { Trans, t } from "@lingui/macro";
import { withI18n } from "@lingui/react";

export const ChangePasswordForm = withI18n()(({ i18n, onSuccess }) => {
  const { register, handleSubmit, reset, errors, setError } = useForm();

  const onSave = (data) => {
    if (data.newUserPassword !== data.newUserPasswordConfirm) {
      reset({ ...data, newUserPasswordConfirm: "" });
      setError(
        "newUserPasswordConfirm",
        "match",
        i18n._(t`The passwords do not match!`)
      );
    } else {
      setLoading(true);
      changePassword(
        data.oldUserPassword,
        data.newUserPassword,
        data.newUserPasswordConfirm
      )
        .then(() => {
          reset();
          setShowSuccess(true);
          setTimeout((_) => onSuccess(), 6000);
        })
        .catch((error) => {
          setError(
            "network",
            "unknown",
            i18n._(t`An unknown error occurred, please reload the page.`)
          );
        })
        .then(() => {
          setLoading(false);
        });
    }
  };

  const [showSuccess, setShowSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  return (
    <FocusLock>
      <form onSubmit={handleSubmit(onSave)}>
        <h3>
          <Trans>Change password:</Trans>
        </h3>
        <div
          className="hintLabel"
          style={{ marginLeft: "var(--universal-margin)" }}
        >
          {errors.network && errors.network.message}
          {errors.newUserPasswordConfirm &&
            errors.newUserPasswordConfirm.message}
        </div>
        <div style={{ marginLeft: "var(--universal-margin)" }}>
          {showSuccess &&
            i18n._(
              t`The password has been changed. You are going to be logged out and can log in with the new password.`
            )}
        </div>
        <input
          data-autofocus={true}
          type="password"
          name="oldUserPassword"
          placeholder={i18n._(t`Current password`)}
          ref={register({ required: true })}
        />
        <input
          type="password"
          name="newUserPassword"
          placeholder={i18n._(t`New password`)}
          ref={register({ required: true })}
        />
        <input
          type="password"
          name="newUserPasswordConfirm"
          placeholder={i18n._(t`Repeat new password`)}
          ref={register({ required: true })}
        />
        <input
          type="submit"
          name="submit"
          value={loading ? i18n._(t`Saving...`) : i18n._(t`Save`)}
        />
      </form>
    </FocusLock>
  );
});
