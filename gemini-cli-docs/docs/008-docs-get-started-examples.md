---
title: Gemini CLI examples
url: https://geminicli.com/docs/get-started/examples
source: crawler
fetched_at: 2026-01-13T19:15:27.392073868-03:00
rendered_js: false
word_count: 455
summary: This document provides examples of how to use Gemini CLI to perform various tasks, including renaming photos, explaining code repositories, combining spreadsheets, and writing unit tests.
tags:
    - gemini-cli
    - examples
    - code-explanation
    - data-manipulation
    - testing
category: tutorial
---

Not sure where to get started with Gemini CLI? This document covers examples on how to use Gemini CLI for a variety of tasks.

**Note:** Results are examples intended to showcase potential use cases. Your results may vary.

## Rename your photographs based on content

[Section titled “Rename your photographs based on content”](#rename-your-photographs-based-on-content)

Scenario: You have a folder containing the following files:

```

photos/photo1.png
photos/photo2.png
photos/photo3.png
```

Give Gemini the following prompt:

```

Rename the photos in my "photos" directory based on their contents.
```

Result: Gemini will ask for permission to rename your files.

Select **Allow once** and your files will be renamed:

```

photos/yellow_flowers.png
photos/antique_dresser.png
photos/green_android_robot.png
```

## Explain a repository by reading its code

[Section titled “Explain a repository by reading its code”](#explain-a-repository-by-reading-its-code)

Scenario: You want to understand how a popular open-source utility works by inspecting its code, not just its README.

Give Gemini CLI the following prompt:

```

Clone the 'chalk' repository from https://github.com/chalk/chalk, read its key source files, and explain how it works.
```

Result: Gemini will perform a sequence of actions to answer your request.

1. First, it will ask for permission to run `git clone` to download the repository.
2. Next, it will find the important source files and ask for permission to read them.
3. Finally, after analyzing the code, it will provide a summary.

Gemini CLI will return an explanation based on the actual source code:

```

The `chalk` library is a popular npm package for styling terminal output with
colors. After analyzing the source code, here's how it works:
-**Core functionality:** The main file sets up a chainable API. Each color or
modifier (like `bold` or `italic`) is a getter that appends the corresponding
ANSI escape code to an internal stack.
-**Chainable API:** When you call `chalk.red.bold('Hello')`, you are accessing
getters. The `red` getter adds the red color code, and the `bold` getter adds
the bold code.
-**Output generation:** When the chain is treated as a string (e.g., in
`console.log`), a final `toString()` method is called. This method joins all
the stored ANSI codes, wraps them around the input string ('Hello'), and adds
a reset code at the end. This produces the final, styled string that the
terminal can render.
```

## Combine two spreadsheets into one spreadsheet

[Section titled “Combine two spreadsheets into one spreadsheet”](#combine-two-spreadsheets-into-one-spreadsheet)

Scenario: You have two .csv files: `Revenue - 2023.csv` and `Revenue - 2024.csv`. Each file contains monthly revenue figures, like so:

```

January,0
February,0
March,0
April,900
May,1000
June,1000
July,1200
August,1800
September,2000
October,2400
November,3400
December,2100
```

You want to combine these two .csv files into a single .csv file.

Give Gemini CLI the following prompt:

```

Combine the two .csv files into a single .csv file, with each year a different column.
```

Result: Gemini CLI will read each file and then ask for permission to write a new file. Provide your permission and Gemini CLI will provide the following .csv:

```

Month,2023,2024
January,0,1000
February,0,1200
March,0,2400
April,900,500
May,1000,800
June,1000,900
July,1200,1000
August,1800,400
September,2000,2000
October,2400,3400
November,3400,1800
December,2100,9000
```

Scenario: You’ve written a simple login page. You wish to write unit tests to ensure that your login page has code coverage.

Give Gemini CLI the following prompt:

```

Write unit tests for Login.js.
```

Result: Gemini CLI will ask for permission to write a new file and create a test for your login page

```

import React from'react';
import { render, fireEvent, waitFor } from'@testing-library/react';
import Login from'./Login';
// Mock the API call for login
jest.mock('./api', () => ({
login: jest.fn(),
}));
describe('Login component', () => {
it('renders the login form correctly', () => {
const { getByLabelText, getByText } =render(<Login />);
expect(getByLabelText('Username')).toBeInTheDocument();
expect(getByLabelText('Password')).toBeInTheDocument();
expect(getByText('Login')).toBeInTheDocument();
});
it('shows an error message with invalid credentials', async () => {
const { getByLabelText, getByText, findByText } =render(<Login />);
constusernameInput=getByLabelText('Username');
constpasswordInput=getByLabelText('Password');
constloginButton=getByText('Login');
// Mock the API to return an error
require('./api').login.mockRejectedValue(newError('Invalid credentials'));
fireEvent.change(usernameInput, { target: { value: 'testuser' } });
fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });
fireEvent.click(loginButton);
consterrorMessage=awaitfindByText('Invalid credentials');
expect(errorMessage).toBeInTheDocument();
});
it('logs in successfully with valid credentials', async () => {
constonLoginSuccess= jest.fn();
const { getByLabelText, getByText } =render(
<LoginonLoginSuccess={onLoginSuccess} />,
);
constusernameInput=getByLabelText('Username');
constpasswordInput=getByLabelText('Password');
constloginButton=getByText('Login');
// Mock the API to return a success message
require('./api').login.mockResolvedValue({ success: true });
fireEvent.change(usernameInput, { target: { value: 'testuser' } });
fireEvent.change(passwordInput, { target: { value: 'correctpassword' } });
fireEvent.click(loginButton);
awaitwaitFor(() => {
expect(onLoginSuccess).toHaveBeenCalled();
});
});
it('disables the submit button while submitting', async () => {
const { getByLabelText, getByText } =render(<Login />);
constusernameInput=getByLabelText('Username');
constpasswordInput=getByLabelText('Password');
constloginButton=getByText('Login');
// Mock the API to have a delay
require('./api').login.mockImplementation(
() =>
newPromise((resolve) =>
setTimeout(() =>resolve({ success: true }), 1000),
),
);
fireEvent.change(usernameInput, { target: { value: 'testuser' } });
fireEvent.change(passwordInput, { target: { value: 'correctpassword' } });
fireEvent.click(loginButton);
expect(loginButton).toBeDisabled();
awaitwaitFor(() => {
expect(loginButton).not.toBeDisabled();
});
});
});
```