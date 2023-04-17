import axios from "axios";
import {useState} from "react";
import {useNavigate} from "react-router-dom";

export default function LoginPage() {
  let navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("")

  async function check_2fa() {
    let auth_token = localStorage.getItem("auth_token");

    if (auth_token === undefined) {
      setError("Some error occured please try again later.");
    } else {
      axios.get("api/check_2fa", {
        headers: {
          Authorization: auth_token,
        }
      })
        .then((response) => {
          console.log(response.data)
          if (response.status === 200 && response.data.is_2fa_activated === true) {
            navigate("validate_totp", {replace: true});
          } else {
            navigate("activate_2fa", {replace: true});
            alert("Successfully logged in. 2FA no activated.")
          }
        })
        .catch((error) => {
          setError("Some error occurred. Please try again later.")
          console.log("error ", error.response)
        })
    }
  }

  async function validate_user() {
    let data = {
      username: username,
      password: password,
    };

    axios
      .post("api/token/login/", data, {})
      .then(function (response) {
        if (response.status === 200) {
          localStorage.setItem("auth_token", "Token " + response.data.auth_token)
          check_2fa();
        }
      })
      .catch(function (error) {
        if (error.response.status === 400) {
          setError("Username or password incorrect.")
        } else {
          setError("Some error occurred. PLease try again later")
        }
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
              <h1 className="text-2xl font-semibold text-center">Sign in</h1>
            </div>
            <div className="divide-y divide-gray-200">
              <form
                className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7"
                onSubmit={(e) => {
                  e.preventDefault();
                  validate_user();
                }}
              >
                <label className="relative">
                  <input
                    autoComplete="off"
                    id="usermname"
                    name="username"
                    type="text"
                    className="peer placeholder-transparent h-12 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:borer-rose-600"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => {
                      setUsername(e.target.value);
                    }}
                  />
                  <label
                    htmlFor="username"
                    className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm"
                  >
                    Username
                  </label>
                </label>
                <div className="relative">
                  <input
                    autoComplete="off"
                    id="password"
                    name="password"
                    type="password"
                    className="peer placeholder-transparent h-12 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:borer-rose-600"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => {
                      setPassword(e.target.value);
                    }}
                  />
                  <label
                    htmlFor="password"
                    className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm"
                  >
                    Password
                  </label>
                </div>
                <div className={"text-sm text-red-500"}>
                  {error}
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
