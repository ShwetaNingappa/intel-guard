import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  VStack,
  Text,
  useToast,
  CheckboxGroup,
  Checkbox,
  SimpleGrid,
} from '@chakra-ui/react';
import { reportIP } from '../services/api';
import { ABUSE_CATEGORIES } from '../types/threat';

const ReportIPForm = ({ initialIP = '' }) => {
  const [ip, setIP] = useState(initialIP);
  const [categories, setCategories] = useState([]);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!ip || categories.length === 0 || !comment) {
      toast({
        title: 'Validation Error',
        description: 'Please fill in all fields',
        status: 'error',
        duration: 3000,
      });
      return;
    }

    setLoading(true);
    try {
      const result = await reportIP({
        ip,
        categories: categories.map(Number),
        comment,
      });

      if (result.success) {
        toast({
          title: 'Report Submitted',
          description: 'IP has been successfully reported to AbuseIPDB',
          status: 'success',
          duration: 5000,
        });
        setCategories([]);
        setComment('');
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      toast({
        title: 'Report Failed',
        description: error.message,
        status: 'error',
        duration: 5000,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={6} borderWidth="1px" borderRadius="lg" bg="gray.800" borderColor="gray.700" shadow="lg">
      <form onSubmit={handleSubmit}>
        <VStack spacing={4} align="stretch">
          <Text fontSize="lg" fontWeight="bold" color="white">
            Report IP to AbuseIPDB
          </Text>

          <FormControl isRequired>
            <FormLabel color="gray.300">IP Address</FormLabel>
            <Input
              value={ip}
              onChange={(e) => setIP(e.target.value)}
              placeholder="Enter IP address"
              bg="gray.900"
              borderColor="gray.600"
              color="white"
              _hover={{ borderColor: 'gray.500' }}
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel color="gray.300">Abuse Categories</FormLabel>
            <CheckboxGroup value={categories} onChange={setCategories}>
              <SimpleGrid columns={2} spacing={2}>
                {Object.entries(ABUSE_CATEGORIES).map(([id, label]) => (
                  <Checkbox key={id} value={id} colorScheme="blue" color="gray.300">
                    {label}
                  </Checkbox>
                ))}
              </SimpleGrid>
            </CheckboxGroup>
          </FormControl>

          <FormControl isRequired>
            <FormLabel color="gray.300">Comment</FormLabel>
            <Textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Describe the abusive activity in detail..."
              rows={4}
              bg="gray.900"
              borderColor="gray.600"
              color="white"
              _hover={{ borderColor: 'gray.500' }}
            />
          </FormControl>

          <Button
            type="submit"
            colorScheme="red"
            isLoading={loading}
            loadingText="Submitting..."
          >
            Submit Report
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default ReportIPForm;
