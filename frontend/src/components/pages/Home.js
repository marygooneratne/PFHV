import React from "react";
import { Box, Card, Typography, Button } from "@material-ui/core";

function Home(props) {
  return (
    <Box className="home-box rows">
      <Box classs="home-info-box">
        <img></img>
        <Box class="home-info-text">
          <Typography variant="body">{props.data}</Typography>
        </Box>
      </Box>
    </Box>
  );
}
