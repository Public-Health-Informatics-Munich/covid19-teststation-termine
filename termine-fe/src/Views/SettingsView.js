import React from "react";
import { ChangePasswordForm } from "../Components/ChangePasswordForm";

export default function SettingsView({ onSuccess }) {
  return (
    <div className="row">
      <ChangePasswordForm onSuccess={onSuccess} />
    </div>
  );
}
