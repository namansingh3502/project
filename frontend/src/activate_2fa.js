import axios from "axios";
import {useEffect, useState} from "react";
import QRCode from "react-qr-code";

export default function Activate2FA() {
  const [totp, setTotp] = useState("");
  const [loading, setLoading] = useState(true);
  const [shaKey, setShaKey] = useState("");
  const [error, setError] = useState("");

  async function validate_totp() {
    let auth_token = localStorage.getItem("auth_token");
    let data = {"totp": totp, "platform": "platform1"};

    axios
      .post("api/validate_otp/", data, {
        headers: {
          Authorization: auth_token,
        }
      })
      .then(function (response) {
        if (response.status === 200) {
          console.log("TOTP validated");
        }
      })
      .catch(function (error) {
        setError("Incorrect key. Please try again.")
        console.log(error.response);
      });
  }

  async function generateKey() {
    let auth_token = localStorage.getItem("auth_token");

    if (auth_token === undefined) {
      setError("Some error occured please try again later.");
    } else {
      axios
        .get("api/generate_sha_key/SHA1", {
          headers: {
            Authorization: auth_token,
          }
        })
        .then(function (response) {
          if (response.status === 200) {
            setShaKey(response.data.sha_key);
            setLoading(false);
          }
        })
        .catch(function (error) {
          setError("Some error occurred. Please try again later.")
          console.log(error);
        });
    }
  }


  useEffect(() => {
    generateKey();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div
          className="absolute inset-0 bg-gradient-to-r from-blue-300 to-blue-600 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div>
              <h1 className="text-2xl font-semibold">
                Activate Two Factor Authentication
              </h1>
            </div>

            <div className="h-auto w-full my-10 flex justify-center items-center">
              {loading ? (
                <div className="h-40 w-40 flex items-center justify-center">
                  <div
                    className="border-t-transparent border-solid animate-spin  rounded-full border-blue-400 border-8 h-36 w-36"></div>
                </div>
              ) : (
                <QRCode
                  className="h-auto w-40"
                  size={256}
                  value={"sshKey"}
                  viewBox={`0 0 256 256`}
                />
              )}
            </div>

            <div className="mt-10">
              <p>Secret Key</p>
              <p>{loading ? "Loading..." : shaKey}</p>
            </div>

            <div className="my-5">
              <div className="py-4">
                <p>Enter auth code</p>
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
                    disabled={loading}
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
