import React from "react";
import { Trans, Plural } from "@lingui/macro";
import { AsLinkIfEmail } from "./AsLinkIfEmail";

export const CouponBox = ({ coupons }) => {
  return (
    <div id="coupons">
      <h3 style={{ paddingLeft: "calc(2 * var(--universal-padding))" }}>
        <div>
          <Trans>
            <Plural
              value={coupons}
              _0="You can book"
              _1="You can still book"
              other="You can still book"
            />
            <b>
              <u>
                <Plural
                  value={coupons}
                  _0="no appointment"
                  _1="one appointment"
                  other="# appointments"
                />
              </u>
            </b>
            <Plural value={coupons} _0="anymore" _1="" other="" />
          </Trans>
        </div>
        {coupons === 0 ? (
          <>
            <div>
              <span className="hintLabel">
                <label>
                  <Trans>In order to book more appointments, contact</Trans>
                  <AsLinkIfEmail value={window.config.contactInfoCoupons} />
                </label>
              </span>
            </div>
          </>
        ) : (
          <div>&nbsp;</div>
        )}
      </h3>
    </div>
  );
};
