from math import ceil

from flask_restful import Api, request


class BaseApi(Api):
    def make_response(self, data, *args, **kwargs):
        status_code = args[0]

        total_data = len(data)
        page = request.args.get("page", None)

        status = "success" if (status_code >= 200 and status_code < 400) else "failed"
        response = {"data": data}

        if "message" in response["data"]:
            response = response["data"]

        if isinstance(data, list) and total_data and page:
            response["pagination"] = {
                "total_data": total_data,
                "total_page": ceil(total_data / len(data)),
                "current_page": page,
            }

        response.update({"status": status, "status_code": status_code})

        response["watermark"] = f"mekarsa © {2022}"

        return super().make_response(response, *args, **kwargs)
