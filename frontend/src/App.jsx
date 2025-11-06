import React, { useState } from 'react';
import {
  ChakraProvider,
  Box,
  Container,
  Heading,
  Input,
  Button,
  VStack,
  HStack,
  Text,
  Spinner,
  Alert,
  AlertIcon,
  AlertDescription,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Grid,
  extendTheme,
} from '@chakra-ui/react';
import { checkIP } from './services/api';
import ThreatScore from './components/ThreatScore';
import SourceScores from './components/SourceScores';
import CategoryList from './components/CategoryList';
import GeoCard from './components/GeoCard';
import RelatedURLs from './components/RelatedURLs';
import ReportIPForm from './components/ReportIPForm';
import VirusTotalURLTable from './components/VirusTotalURLTable';
import RawDataViewer from './components/RawDataViewer';

// Dark mode theme configuration
const config = {
  initialColorMode: 'dark',
  useSystemColorMode: false,
};

const theme = extendTheme({
  config,
  styles: {
    global: {
      body: {
        bg: 'gray.900',
        color: 'white',
      },
    },
  },
});

function App() {
  const [ipAddress, setIPAddress] = useState('');
  const [threatData, setThreatData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!ipAddress.trim()) {
      setError('Please enter a valid IP address');
      return;
    }

    // Validate IP format
    const ipPattern = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (!ipPattern.test(ipAddress.trim())) {
      setError('Invalid IP address format. Please enter a valid IPv4 address (e.g., 8.8.8.8)');
      return;
    }

    // Check for reserved/private IP ranges
    const octets = ipAddress.trim().split('.').map(Number);
    
    // Validate octet ranges
    if (octets.some(octet => octet < 0 || octet > 255)) {
      setError('Invalid IP address. Each octet must be between 0 and 255.');
      return;
    }

    // Block private/reserved ranges
    if (
      // 169.254.0.0/16 (Link-Local/AWS metadata)
      (octets[0] === 169 && octets[1] === 254) ||
      // 10.0.0.0/8 (Private)
      (octets[0] === 10) ||
      // 172.16.0.0/12 (Private)
      (octets[0] === 172 && octets[1] >= 16 && octets[1] <= 31) ||
      // 192.168.0.0/16 (Private)
      (octets[0] === 192 && octets[1] === 168) ||
      // 127.0.0.0/8 (Loopback)
      (octets[0] === 127) ||
      // 0.0.0.0/8 (Reserved)
      (octets[0] === 0) ||
      // 224.0.0.0/4 (Multicast)
      (octets[0] >= 224 && octets[0] <= 239) ||
      // 240.0.0.0/4 (Reserved)
      (octets[0] >= 240)
    ) {
      setError('Cannot analyze private, reserved, or link-local IP addresses. Please enter a public IP address.');
      return;
    }

    setLoading(true);
    setError(null);
    setThreatData(null);

    try {
      const data = await checkIP(ipAddress.trim());
      setThreatData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <ChakraProvider theme={theme}>
      <Box bg="gray.900" minH="100vh" py={8}>
        <Container maxW="container.xl">
          <VStack spacing={8} align="stretch">
            {/* Header */}
            <Box textAlign="left" p={6} bg="gray.800" borderRadius="lg" borderWidth="1px" borderColor="#2A2F3A" boxShadow="0 0 0 1px #2A2F3A, 0 0 20px rgba(0,255,255,0.10)">
              <Heading 
                size="xl" 
                mb={1} 
                color="cyan.300"
                textShadow="0 0 12px rgba(0,255,255,0.35)"
                letterSpacing="widest"
              >
                TechSpark's vision Engine
              </Heading>
              <Text color="cyan.100" fontSize="sm" mb={4}>TICE - Threat Intelligence Dashboard</Text>

              <HStack spacing={4}>
                <Input
                  placeholder="Enter suspicious IP"
                  size="md"
                  value={ipAddress}
                  onChange={(e) => setIPAddress(e.target.value)}
                  onKeyPress={handleKeyPress}
                  bg="gray.900"
                  borderColor="gray.600"
                  _hover={{ borderColor: 'cyan.400' }}
                  _focus={{ borderColor: 'cyan.300', boxShadow: '0 0 0 1px #00B5D8' }}
                  color="white"
                />
                <Button
                  colorScheme="red"
                  size="md"
                  onClick={handleSearch}
                  isLoading={loading}
                  loadingText="Lookup..."
                  minW="120px"
                >
                  Lookup
                </Button>
              </HStack>
            </Box>

            {/* Loading State */}
            {loading && (
              <Box textAlign="center" py={12}>
                <Spinner size="xl" color="blue.500" thickness="4px" />
                <Text mt={4} fontSize="lg" color="gray.400">
                  Aggregating threat intelligence from 8 sources...
                </Text>
                <Text mt={2} fontSize="sm" color="gray.500">
                  AI analysis in progress
                </Text>
              </Box>
            )}

            {/* Error State */}
            {error && (
              <Alert status="error" borderRadius="lg" bg="red.900" borderColor="red.500" borderWidth="1px">
                <AlertIcon />
                <AlertDescription color="red.200">{error}</AlertDescription>
              </Alert>
            )}

            {/* Results */}
            {threatData && !loading && (
              <VStack spacing={6} align="stretch">
                {/* Top Row: Score + Categories */}
                <Grid templateColumns={{ base: '1fr', lg: 'repeat(2, 1fr)' }} gap={6}>
                  <ThreatScore score={threatData.final_threat_score} rationale={threatData.ai_rationale} />
                  <CategoryList reputation={threatData.reputation} rationale={threatData.ai_rationale} />
                </Grid>

                {/* Middle Row: Source Scores + Geolocation */}
                <Grid templateColumns={{ base: '1fr', lg: 'repeat(2, 1fr)' }} gap={6}>
                  <SourceScores reputation={threatData.reputation} ownership={threatData.ownership} />
                  <GeoCard geolocation={threatData.geolocation} />
                </Grid>

                {/* Bottom Row: Related URLs (compact) + Detailed table */}
                <Grid templateColumns={{ base: '1fr', lg: 'repeat(2, 1fr)' }} gap={6}>
                  <RelatedURLs urls={threatData.virustotal_related_urls} />
                  {Array.isArray(threatData.virustotal_related_urls) && threatData.virustotal_related_urls.length > 0 && (
                    <VirusTotalURLTable urls={threatData.virustotal_related_urls} />
                  )}
                </Grid>

                {/* Tabs for Additional Features */}
                <Tabs variant="enclosed" colorScheme="blue">
                  <TabList borderColor="gray.700">
                    <Tab _selected={{ bg: 'gray.800', color: 'blue.400' }} color="gray.400">Report IP</Tab>
                    <Tab _selected={{ bg: 'gray.800', color: 'blue.400' }} color="gray.400">Raw Data</Tab>
                  </TabList>

                  <TabPanels>
                    <TabPanel px={0}>
                      <ReportIPForm initialIP={threatData.ip_address} />
                    </TabPanel>
                    <TabPanel px={0}>
                      <RawDataViewer rawData={threatData.raw_data} ip={threatData.ip_address} />
                    </TabPanel>
                  </TabPanels>
                </Tabs>
              </VStack>
            )}
          </VStack>
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App;
