import React from "react";
import { Trans } from "@lingui/macro";
import { InputRequired } from "./InputRequired";

export const AddressForm = ({ form, disable }) => {
  const { register, errors } = form;
  if (window.config.formFields.includes("address")) {
    return (
      <fieldset className="input-group vertical">
        <legend>
          <Trans>Home Address</Trans>
        </legend>
        <div className="displayFlex vertical">
          <div className="displayFlex justifyBetween">
            <label htmlFor="street">
              <Trans>Street</Trans> {errors.street && <InputRequired />}
            </label>
            <label htmlFor="streetnumber">
              <Trans>StreetNumber</Trans>{" "}
              {errors.streetNumber && <InputRequired />}
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
              <Trans>PostCode</Trans> {errors.postCode && <InputRequired />}
            </label>
            <label htmlFor="city">
              <Trans>City</Trans> {errors.city && <InputRequired />}
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
    );
  } else {
    return <React.Fragment />;
  }
};
