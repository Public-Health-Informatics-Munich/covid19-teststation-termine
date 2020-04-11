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
              zero="You can book"
              other="You can still book"
            />
            <b>
              <u>
                <Plural
                  value={coupons}
                  zero="no appointment"
                  one="{coupons} appointment"
                  other="{coupons} appointments"
                />
              </u>
            </b>
            <Plural value={coupons} zero="anymore" other="" />
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
