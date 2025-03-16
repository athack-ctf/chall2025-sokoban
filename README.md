# @HACK 2025: Sokobaaaan

> Authored by [Hugo](https://github.com/hkerma).

- **Category**: `Miscellaneous`
- **Value**: `150 points`
- **Tags**: `beginner` `tcp`

> Roger is supposed to work on his quantum chromodynamics assignment for tomorrow... but instead he decided to solve Sokoban games.
> What a waste of time, right? I hope his supervisor never finds out.
> 
> 
> NOTE:
> - `@` player
> - `$` box
> - `.` goal
> - `#` wall
> - `*` box on goal
> - `+` player on goal
> 
> For each puzzle, the answer is expected as a sequence of move, such as `urRlddDlLuuuL` for instance.
> u, d, l, r = up, down, left, right
> UPPERCASE = push a box, lowercase = move
> 
> Solutions are not unique.
> 

## Access a dockerized instance

Run challenge container using docker compose
```
docker compose up -d
```
Connect to the TCP socket (e.g., using nc command)
```
nc localhost 52019 
```
<details>
<summary>
How to stop/restart challenge?
</summary>

To stop the challenge run
```
docker compose stop
```
To restart the challenge run
```
docker compose restart
```

</details>


## Reveal Flag

Did you try solving this challenge?
<details>
<summary>
Yes
</summary>

Did you **REALLY** try solving this challenge?

<details>
<summary>
Yes, I promise!
</summary>

Flag: `ATHACKCTF{G0dIHateTh3s3StuFF}`

</details>
</details>


---

## About @HACK
[@HACK](https://athackctf.com/) is an annual CTF (Capture The Flag) competition hosted by [HEXPLOIT ALLIANCE](https://hexploit-alliance.com/) and [TECHNATION](https://technationcanada.ca/) at Concordia University in Montreal, Canada.

---
[Check more challenges from @HACK 2025](https://github.com/athack-ctf/AtHackCTF-2025-Challenges).