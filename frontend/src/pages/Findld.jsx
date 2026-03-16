import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Stack,
  TextField,
  Typography,
  Alert,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function FindId() {
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");

  const [emailSent, setEmailSent] = useState(false);
  const [verified, setVerified] = useState(false);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [timeLeft, setTimeLeft] = useState(0);
  const [userIds, setUserIds] = useState([]);

  // mm:ss 변환
  const formatTime = (seconds) => {
    const min = String(Math.floor(seconds / 60)).padStart(2, "0");
    const sec = String(seconds % 60).padStart(2, "0");
    return `${min}:${sec}`;
  };

  // 카운트다운
  useEffect(() => {
    if (timeLeft <= 0) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          setError("요청 시간이 초과되었습니다. 임시 코드를 재발급해주세요.");
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  // 인증코드 발송 / 재발급
  const handleSendCode = async () => {
    setError("");
    setMessage("");
    setVerified(false);
    setUserIds([]);
    setCode("");

    if (!email.trim()) {
      setError("이메일을 입력해주세요.");
      return;
    }

    if (!EMAIL_REGEX.test(email)) {
      setError("올바른 이메일 형식을 입력해주세요.");
      return;
    }

    try {
      const response = await fetch("/api/find-id/send-code", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "이메일 인증 요청에 실패했습니다.");
        return;
      }

      setEmailSent(true);
      setTimeLeft(300); // 5분
      setMessage("임시 코드가 이메일로 전송되었습니다.");
    } catch (err) {
      setError("서버 오류가 발생했습니다.");
    }
  };

  // 인증코드 확인
  const handleVerifyCode = async () => {
    setError("");
    setMessage("");
    setUserIds([]);

    if (!emailSent) {
      setError("먼저 임시 코드를 발급받아주세요.");
      return;
    }

    if (timeLeft <= 0) {
      setError("요청 시간이 초과되었습니다. 임시 코드를 재발급해주세요.");
      return;
    }

    if (!code.trim()) {
      setError("임시 코드를 입력해주세요.");
      return;
    }

    try {
      const response = await fetch("/api/find-id/verify-code", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, code }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "임시 코드 검증에 실패했습니다.");
        return;
      }

      setVerified(true);
      setUserIds(data.userIds || []);
      setMessage("이메일 인증이 완료되었습니다.");
    } catch (err) {
      setError("서버 오류가 발생했습니다.");
    }
  };

  return (
    <Box sx={{ maxWidth: 500, mx: "auto", mt: 8 }}>
      <Card sx={{ borderRadius: 3 }}>
        <CardContent>
          <Typography variant="h5" fontWeight="bold" mb={3}>
            아이디 찾기
          </Typography>

          <Stack spacing={2}>
            <TextField
              label="이메일"
              fullWidth
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={verified}
            />

            <Button
              variant="contained"
              onClick={handleSendCode}
              disabled={verified}
            >
              {emailSent ? "임시 코드 재발급" : "임시 코드 발송"}
            </Button>

            {emailSent && (
              <>
                <Stack direction="row" spacing={1} alignItems="center">
                  <TextField
                    label="임시 코드 입력"
                    fullWidth
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    disabled={verified}
                  />
                  <Button
                    variant="outlined"
                    onClick={handleSendCode}
                    disabled={verified}
                    sx={{ minWidth: 100, height: 56 }}
                  >
                    재발급
                  </Button>
                  <Typography
                    sx={{
                      minWidth: 60,
                      textAlign: "center",
                      fontWeight: "bold",
                    }}
                  >
                    {formatTime(timeLeft)}
                  </Typography>
                </Stack>

                <Button
                  variant="contained"
                  color="success"
                  onClick={handleVerifyCode}
                  disabled={verified}
                >
                  인증 확인
                </Button>
              </>
            )}

            {message && <Alert severity="success">{message}</Alert>}
            {error && <Alert severity="error">{error}</Alert>}

            {verified && userIds.length > 0 && (
              <Box mt={2}>
                <Typography variant="h6" fontWeight="bold" mb={1}>
                  가입된 아이디 목록
                </Typography>
                <List>
                  {userIds.map((id, index) => (
                    <ListItem key={index} divider>
                      <ListItemText primary={id} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            {verified && userIds.length === 0 && (
              <Alert severity="warning">
                인증은 완료되었지만 해당 이메일에 연결된 아이디가 없습니다.
              </Alert>
            )}
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
}

export default FindId;
