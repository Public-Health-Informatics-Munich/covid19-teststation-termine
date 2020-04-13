import React from "react";
import { Trans, Plural } from "@lingui/macro";

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
            <div
              dangerouslySetInnerHTML={{
                __html: window.config.contactInfoCoupons,
              }}
            />
          </>
        ) : (
          <div>&nbsp;</div>
        )}
      </h3>
    </div>
  );
};
