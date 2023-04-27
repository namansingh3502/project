import axios from "axios";
import {useState} from "react";

export default function Validate_TOTP() {
  const [totp, setTotp] = useState("");
  const [error, setError] = useState("")
  async function validate_totp() {
    let auth_token = localStorage.getItem("auth_token")
    let data = {totp: totp, platform: localStorage.getItem("platform")};
    axios
      .post("api/validate_otp/", data, {
        headers: {
          Authorization: auth_token,
        }
      })
      .then(function (response) {
        if (response.status === 200) {
          if(response.data.is_valid === true){
            alert("Authentication key verified successfully.")
          }
          else{
            setError("Invalid authentication key.")
          }
        }
      })
      .catch(function (error) {
        console.log("error occured", error);
      });
  }

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div
          className="absolute inset-0 bg-gradient-to-r from-blue-300 to-blue-600 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div>
              <h1 className="text-2xl font-semibold">
                Two Factor Authentication
              </h1>
            </div>

            <div className="my-10">
              <div className="py-4">
                <p>Enter authentication code</p>
              </div>
              <div className={"text-red-500 text-sm my-4"}>
                {error}
              </div>
              <form
                className="pb-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7"
                onSubmit={(e) => {
                  e.preventDefault();
                  validate_totp();
                }}
              >
                <div className="relative">
                  <input
                    autoComplete="off"
                    id="totp"
                    name="totp"
                    type="text"
                    className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:borer-rose-600"
                    placeholder="XXXXXX"
                    value={totp}
                    maxLength={6}
                    onChange={(e) => {
                      if (
                        (e.target.value >= "0" && e.target.value <= "9") ||
                        e.target.value === ""
                      ) {
                        setTotp(e.target.value);
                      }
                    }}
                  />
                  <label
                    htmlFor="password"
                    className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm"
                  >
                    XXXXXX
                  </label>
                </div>
                <div className="relative">
                  <button
                    className="bg-blue-500 text-white rounded-md px-2 py-1"
                    type="submit"
                  >
                    Submit
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
