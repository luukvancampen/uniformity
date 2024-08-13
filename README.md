# Uniformity

Many great digital forensic platforms have been created by the open-source community.
To expand the capabilities of a digital forensic platform, developers can integrate other digital forensic platforms into their own platform. A key benefit of this approach is that digital forensic knowledge is reused, which means time and money can be spent on creating new knowledge, such as support for more file formats
As it turns out, integrating digital forensic platforms into each other is a difficult task. One commonly applicable reason for this is the fact that the output of digital forensic platforms is often not uniform. This makes mapping the output of a platform to that of another difficult. Other complicating factors are:
- No explicit data model
- No documentation of structure of output
- No documentation of meaning of output
- No documentation of supported formats

By failing to provide a uniform output and thus promoting interoperability among tools, developers miss out on chance to improve the digital forensics community as a whole. 

## So what is this then?

This Github repository contains a tool that can be used to quantify how uniform the output of a digital forensic platform is. 

### Cool, why would I want to use it?

If you are developing an open-source digital forensic platform and you care about the interoperability of your tool, you likely want your tool to produce a uniform output. Since it's difficult to assess that yourself in an objective manner, you can use this tool to do it for you!

### Cool, I want to know all the ins and outs. Where are they?

In my Master's thesis! It'll be out soon.

### Cool, how does it work? 

It's quite fool-proof! The tool parses the output of your platform and starts computing. To compute uniformity, "similarity" between several aspects of your data has to be computed. For example, the tool might need to know whether the timestamp values `1723582227` and `Tuesday 13 August 2024 20:50:27` contain the exact same amount of information.
To determine this, the tool needs two sources of knowledge. The first source is one that is capable of understanding timestamp values in both notations. In our tool, this is a large language model from OpenAI. Secondly, the tool needs to know more specifically when things are similar. It needs to know this because the question whether these timestamp values contain the exact same amount of information is not answerable without more knowledge!
One person might answer "yes", because they represent the same point in time. Another person might answer "no", because the human readable timestamp contains the day and month of that point in time spelled out. Both answers would be right! 

To counteract this problem, the user needs to specify so-called `problem-specific knowledge`. This can be done by altering the prompts in `prompts.py` such that the frame of reference from which to determine whether things are similar or not, becomes clear for the LLM.

### Cool, so what exact steps do I need to take?
1. In your virtual environment, set the environment variable `OPENAI_API_KEY` to your OpenAI api key
1. Put the output of your tool in the ./input directory. Currently, this directory contains a sample input.
2. Change the prompts in `prompts.py` so they can be used to accurately determine whether things are similar or not
3. Execute the `main()` function in `main.py`.
4. If the large language model can not make a decision on whether things are similar, you are prompted to make a decision. If so, answer. 
5. Done!

> [!IMPORTANT]
> Although as much as possible has been optimised, this tool requires making many calls to the OpenAI API, namely O(N^2) over the number of columns.
> Because of this, you may encounter issues with rate-limiting and high costs.