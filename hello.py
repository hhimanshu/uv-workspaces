import httpx


def main():
    print("Hello from uv-hello-world!")
    r = httpx.get("https://www.example.com")
    print(r.status_code)


if __name__ == "__main__":
    main()
