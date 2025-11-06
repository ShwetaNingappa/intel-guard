import React from 'react';
import { Box, Text, VStack, HStack, Badge } from '@chakra-ui/react';

const Card = (props) => (
  <Box
    p={4}
    borderWidth="1px"
    borderRadius="lg"
    bg="gray.800"
    borderColor="#2A2F3A"
    boxShadow="0 0 0 1px #2A2F3A, 0 0 16px rgba(0,255,255,0.08)"
    {...props}
  />
);

const GeoCard = ({ geolocation = {} }) => {
  const country = geolocation.ip_api_country || geolocation.ipstack_country || 'Unknown';
  const isp = geolocation.ip_api_isp || geolocation.ipstack_isp || 'Unknown';
  const hosting = geolocation.consensus_hosting_flag ? 'Yes' : 'No';

  return (
    <Card>
      <VStack align="stretch" spacing={4}>
        <Text fontSize="lg" fontWeight="bold" color="white">Geolocation</Text>

        {/* Stylized mini world map */}
        <Box h="140px" bg="gray.900" borderRadius="md" borderWidth="1px" borderColor="#2A2F3A" position="relative" overflow="hidden">
          <svg width="100%" height="100%" viewBox="0 0 300 140" preserveAspectRatio="xMidYMid meet">
            <defs>
              <linearGradient id="grid" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#1F2937" />
                <stop offset="100%" stopColor="#111827" />
              </linearGradient>
            </defs>
            <rect x="0" y="0" width="300" height="140" fill="url(#grid)" />
            {/* simple dotted map silhouettes */}
            <g fill="#2D3748">
              <circle cx="70" cy="70" r="28" />
              <ellipse cx="155" cy="60" rx="42" ry="26" />
              <ellipse cx="230" cy="78" rx="30" ry="20" />
            </g>
            {/* glow dot */}
            <g>
              <circle cx="200" cy="80" r="4" fill="#F56565" />
            </g>
          </svg>
        </Box>

        <VStack align="stretch" spacing={1}>
          <HStack justify="space-between"><Text color="gray.400">Country</Text><Text color="gray.200">{country}</Text></HStack>
          <HStack justify="space-between"><Text color="gray.400">ISP</Text><Text color="gray.200">{isp}</Text></HStack>
          <HStack justify="space-between"><Text color="gray.400">Hosting/DC</Text><Badge colorScheme={hosting === 'Yes' ? 'orange' : 'blue'}>{hosting}</Badge></HStack>
        </VStack>
      </VStack>
    </Card>
  );
};

export default GeoCard;
