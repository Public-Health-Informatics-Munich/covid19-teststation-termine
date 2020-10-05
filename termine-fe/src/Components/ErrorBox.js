import React from "react";
import { Trans } from "@lingui/macro";

export const ErrorBox = ({ errorMessage }) => {
  return (
    <div className="card error fluid">
      <div className="section">
        <h3 className="doc">
          <Trans>An error occurred</Trans>
        </h3>
        <p className="doc">{errorMessage}</p>
      </div>
    </div>
  );
};
