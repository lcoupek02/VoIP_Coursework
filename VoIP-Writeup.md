---


---

<h1 id="voip-coursework">VoIP Coursework</h1>
<blockquote>
<p><strong>Note:</strong> All attacks run under the assumption that attacker has access to the same LAN as victims and all machines  are run off a <strong>private</strong> hotspot.</p>
</blockquote>
<h2 id="lab-set-up">Lab Set-up</h2>
<p>The lab for the VoIP attacks consisted of:</p>
<ul>
<li>Two Zoiper Clients</li>
<li>Tribox VM</li>
<li>Attacker VM (Kali Linux)</li>
</ul>
<blockquote>
<p>Zoiper is a free to use VoIP softphone, this means it allows users to make telephones call via the internet.<br>
Tribox is telephone based system based on the Asterisk PBX software and allows clients to make VoIP calls, it also comes with a pre-made GUI for settings control</p>
</blockquote>
<h2 id="voip-eavsdropping">VoIP Eavsdropping</h2>
<h3 id="the-attack">The Attack</h3>
<p>When the attacker is on the same network as VoIP communications it is possible to use a network protocol analyser such as wireshark to sniff the packets being sent over the network. On the attacker machine follow these steps on wireshark:</p>
<ol>
<li>Filters on wireshark can be utilised to isolate VoIP packets, by filtering for only <strong>RTP packets</strong>, VoIP communication can be identified.</li>
<li>Once the RTP packets have been found select <em>Telephony</em> -&gt; <em>RTP</em> -&gt; <em>RTP player</em> , this will play back the audio from one side of the call</li>
<li>Identify which side of the the call you listened too - it will be the IP source of the packet you selected in Step 2.</li>
<li>Then filter wireshark for the destination IP of that packet.</li>
<li>Repeat Step 2 to listen to other side of the call,</li>
</ol>
<h3 id="why-it-works">Why It Works</h3>
<p>This attack is effective due to the inherent vulnerabilities in VoIP protocols, particularly in how RTP transmits audio streams. Some other vulnerabilities include:</p>
<ul>
<li>Lack of Encryption: By default RTP packets are transmitted in plaintext meaning they are unecrypted so can be easily capatured and interpreted by anyone on the same network</li>
<li>Insufficient Network Segmentation: VoIP networks are often poorly segmented from the main data network, making it easy for attackers on the same LAN to access VoIP traffic. Without the proper VLANs. the VoIP packets are exposed for everyone to sniff on the main network</li>
<li>Easy to capture: RTP packets used predictable port ranges (6384–3276) or if dynamic ports have been turned off (5060 for RTP based on UDP) making them easy to filter and identify. Its easy for attackers to use tools like Wireshark to capture and reassemble RTP packets with minimal effort</li>
</ul>
<h3 id="countermeasures">Countermeasures</h3>
<p>To counteract this attack several countermeasures can be used:</p>
<ul>
<li>Use SRTP (Secure Real-time Transport Protocol) : This protocol provides encryption, authentication, message integrity, and protection against replay attacks for RTP data.</li>
<li>Use VLAN : Seperate VoIP system from main LAN reducing access to it.</li>
</ul>
<h2 id="voip-ennumeration-and-cracking">VoIP Ennumeration and Cracking</h2>
<h3 id="the-attack-1">The Attack</h3>
<p>This attack involves gathering information about a VoIP server such as extensions connected to the server, IP and port addresses. Then using this information to crack users passwords to provide access to their accounts, this can be used in a variety of attacks such as masquerading.<br>
The attack can be complete by following these steps on the attacker VM :</p>
<ol>
<li>Use command <em>ifconfig</em> and take note of the netmask and IP network</li>
<li>Download the tool SipVicious - on Kali Linux this can be done with the command <em>sudo apt install sipvicious</em></li>
</ol>
<blockquote>
<p>SipVicious is a VoIP security tool used in peneration testing of VoIP services by security teams by can be used for malicious purposes</p>
</blockquote>
<ol start="3">
<li>
<p>Use the SipVicious command <em>svmap IP Network</em> , for example <em>svmap 192.168.1.0/24</em> if IP mask is 255.255.255.0.  This will reveal the IP address of any VoIP server (such as asterisk) on the network.</p>
</li>
<li>
<p>Use the SipVicious command <em>svwar -e <strong>extension range</strong> <strong>IP of VoIP server</strong> -m INVITE</em> to find the any extensions (clients) connected to the server</p>
</li>
<li>
<p>Finally use the SipVicious command <em>svcrack -u <strong>extension number</strong> <strong>IP of VoIP Server</strong></em> to try to crack the password to the extensions you found.</p>
</li>
</ol>
<blockquote>
<p>Scripts could be created to automate and streamline these commands</p>
</blockquote>
<h3 id="whyhow--it-works">Why/How  it works</h3>
<ul>
<li>Svmap: By default this command sends <strong>SIP OPTIONS</strong> requests to all the IP addresses specified and listens on port 5060 for responses. It then checks for responses from SIP devices. This command is highly  customisable - you can specify which ports are listened to with the <em>-p</em> flag, which message (change it to INVITE or REGISTER with the <em>-m</em> flag and many more options.</li>
</ul>
<blockquote>
<p>The <strong>OPTIONS</strong> method is a SIP command that asks for the device’s capabilities (used for device health checks).</p>
</blockquote>
<ul>
<li>Svwar:  This commands can scan for large ranges of numeric extensions, scan for extensions for a .txt file containing list of possible ones and use different SIP request methods (<em>-m</em>) as not all VoIP servers behave the same. Like Svamp this command is highly customisble to suite the users needs. In the command used in this demo, svwar sends <strong>SIP INVITE</strong> requests to the specified range of extensions and then checks for valid responses. It then returns a list of available extensions and also says if it requires authication or not, this is found from the response of the server. For example  -   <code>401 Unauthorized</code> means the extension <strong>requires authentication</strong> (it prompts for credentials)  while <code>200 OK</code> means the extension <strong>does NOT require authentication</strong> (open extension).</li>
</ul>
<blockquote>
<p>The <strong>INVITE</strong> method is a sip command that tries to initiate a SIP call</p>
</blockquote>
<ul>
<li>Svcrack: This sends <strong>SIP REGISTER</strong> requests to the specified extension. The default password set for svcrack` is a numeric integer set ranging from 100 to 999 but the flag <em>-D</em> can be used for scanning for default/weak password or <em>-d dictonary.txt</em> can be used to scan using a custom list of passwords. <em>-m</em> can be used to change to <strong>INVITE</strong> as devices may not response to <strong>REGISTER</strong>  The command then listens to the repsonse to see if the credential input was successfull</li>
</ul>
<blockquote>
<p>The <strong>REGISTER</strong> method is a sip command to register a user against a SIP server</p>
</blockquote>
<h3 id="countermeasures-1">Countermeasures</h3>
<p>To counteract this attack several countermeasures can be used:</p>
<ul>
<li>The <em>iptables</em> commands can be used to configure the kernels firewall. By using the commands:
<ul>
<li><em>iptables -A INPUT -p udp --dport 5060 -m state --state NEW -m recent --set</em></li>
<li><em>iptables -A INPUT -p udp --dport 5060 -m state --state NEW -m recent --update --seconds 60 --hitcount 10 -j DROP</em></li>
</ul>
</li>
<li>This can block repeated SIP login attemps by only allowing up to 10 new SIP connections a minute and blocking IPs exceeding that threshold hold.</li>
<li>IP Tables can also be used to rate limit SIP requests making brute force attacks ineffective with these commands:
<ul>
<li><em>iptables -A INPUT -p udp --dport 5060 -m limit --limit 5/s --limit-burst 10 -j ACCEPT</em><br>
<em>-iptables -A INPUT -p udp --dport 5060 -j DROP</em></li>
</ul>
</li>
<li>Make sure to use <em>service iptables save</em> to save the newly created rules</li>
</ul>
<blockquote>
<p>Unfortuantely this only blocks the svcrack attacks but information gathering commands like svmap still prove to be useful</p>
</blockquote>
<ul>
<li>To completely block <strong>all attack methods</strong>, anonymous call acceptance must be disabled.</li>
<li>With Tribox acting as the VoIP server this can be done in the web GUI <em>General Settings</em> tab or in the <em>sip.conf/sip_general_custom.conf</em> file set <strong>allowguest=no</strong></li>
<li>This prevents Asterisk from accepting calls from unauthenticated sources (anonymous SIP calls) - like the ones coming from SipVicious</li>
</ul>

