import React from 'react';
import { Box, Text, VStack } from '@chakra-ui/react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const DetectionChart = ({ virustotal }) => {
  const data = [
    { name: 'Malicious', value: virustotal?.malicious ?? 0 },
    { name: 'Suspicious', value: virustotal?.suspicious ?? 0 },
    { name: 'Harmless', value: virustotal?.harmless ?? 0 },
    { name: 'Undetected', value: virustotal?.undetected ?? 0 },
  ];

  return (
    <Box p={6} borderWidth="1px" borderRadius="lg" bg="gray.800" borderColor="gray.700" shadow="lg">
      <VStack align="stretch" spacing={4}>
        <Text fontSize="lg" fontWeight="bold" color="white">VirusTotal Detections</Text>
        <Box h="250px">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" fill="#3182CE" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </VStack>
    </Box>
  );
};

export default DetectionChart;
